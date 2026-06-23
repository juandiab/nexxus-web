from __future__ import annotations

import base64
import json
import os
from typing import Any

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

SCSTUDIO_DB_CRYPTO_VERSION = 1
SCSTUDIO_DB_CRYPTO_SALT = b"nexxus-tech-scstudio-db-v1"
SCSTUDIO_DB_CRYPTO_INFO = b"scstudio-db-sync-v1"


def derive_scstudio_db_key(server_fingerprint: str) -> bytes:
    ikm = server_fingerprint.strip().encode("utf-8")
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SCSTUDIO_DB_CRYPTO_SALT,
        info=SCSTUDIO_DB_CRYPTO_INFO,
    ).derive(ikm)


def encrypt_scstudio_database(server_fingerprint: str, payload: dict[str, Any]) -> str:
    key = derive_scstudio_db_key(server_fingerprint)
    nonce = os.urandom(12)
    plaintext = json.dumps(payload, separators=(",", ":"), default=str).encode("utf-8")
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, None)
    blob = bytes([SCSTUDIO_DB_CRYPTO_VERSION]) + nonce + ciphertext
    return base64.urlsafe_b64encode(blob).decode("ascii")


def decrypt_scstudio_database(server_fingerprint: str, encrypted: str) -> dict[str, Any]:
    padded = encrypted + "=" * (-len(encrypted) % 4)
    blob = base64.urlsafe_b64decode(padded.encode("ascii"))
    if not blob or blob[0] != SCSTUDIO_DB_CRYPTO_VERSION:
        raise ValueError("Unsupported or invalid SC Studio database payload version.")
    nonce = blob[1:13]
    ciphertext = blob[13:]
    key = derive_scstudio_db_key(server_fingerprint)
    plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)
    return json.loads(plaintext.decode("utf-8"))
