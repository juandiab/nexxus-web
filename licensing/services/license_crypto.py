from __future__ import annotations

import base64
import json
import os
from typing import Any

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

LICENSE_CRYPTO_VERSION = 1
LICENSE_CRYPTO_SALT = b"nexxus-tech-license-v1"
LICENSE_CRYPTO_INFO = b"license-payload"


def normalize_license_code(code: str) -> str:
    return code.strip().upper().replace("-", "")


def derive_license_key(app_fingerprint: str, license_code: str) -> bytes:
    ikm = f"{app_fingerprint.strip()}:{normalize_license_code(license_code)}".encode("utf-8")
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=LICENSE_CRYPTO_SALT,
        info=LICENSE_CRYPTO_INFO,
    ).derive(ikm)


def encrypt_license_payload(
    app_fingerprint: str,
    license_code: str,
    payload: dict[str, Any],
) -> str:
    key = derive_license_key(app_fingerprint, license_code)
    nonce = os.urandom(12)
    plaintext = json.dumps(payload, separators=(",", ":"), default=str).encode("utf-8")
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, None)
    blob = bytes([LICENSE_CRYPTO_VERSION]) + nonce + ciphertext
    return base64.urlsafe_b64encode(blob).decode("ascii")


def decrypt_license_payload(
    app_fingerprint: str,
    license_code: str,
    encrypted: str,
) -> dict[str, Any]:
    padded = encrypted + "=" * (-len(encrypted) % 4)
    blob = base64.urlsafe_b64decode(padded.encode("ascii"))
    if not blob or blob[0] != LICENSE_CRYPTO_VERSION:
        raise ValueError("Unsupported or invalid license payload version.")
    nonce = blob[1:13]
    ciphertext = blob[13:]
    key = derive_license_key(app_fingerprint, license_code)
    plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)
    return json.loads(plaintext.decode("utf-8"))
