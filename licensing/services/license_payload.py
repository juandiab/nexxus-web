from __future__ import annotations

from datetime import datetime
from typing import Any

from crypto import decrypt
from services.license_crypto import encrypt_license_payload
from utils.time import ensure_utc_aware


def plain_license_code(stored: str) -> str:
    try:
        return decrypt(stored)
    except ValueError:
        return str(stored).strip()


def format_utc(value: datetime) -> str:
    aware = ensure_utc_aware(value)
    return aware.strftime("%Y-%m-%dT%H:%M:%SZ")


def expiration_unix(value: datetime | None) -> int | None:
    if value is None:
        return None
    return int(ensure_utc_aware(value).timestamp())


def build_license_payload(doc: dict[str, Any], plain_code: str) -> dict[str, Any]:
    registration = doc.get("registrationDate")
    expiration = doc.get("expirationDate")
    fingerprint = doc.get("appFingerprint") or ""
    return {
        "licenseCode": plain_code,
        "licenseType": doc.get("licenseType", "free"),
        "usageType": doc.get("usageType"),
        "validityDays": doc.get("validityDays"),
        "registrationDate": format_utc(registration) if registration else None,
        "expirationDate": format_utc(expiration) if expiration else None,
        "expirationDateUnix": expiration_unix(expiration),
        "renewalCount": int(doc.get("renewalCount") or 0),
        "name": doc.get("name", ""),
        "email": doc.get("email", ""),
        "company": doc.get("company", ""),
        "application": doc.get("application", ""),
        "appFingerprint": fingerprint,
        "appName": doc.get("appName") or doc.get("application"),
        "activationDate": doc.get("activationDate"),
    }


def build_encrypted_license(doc: dict[str, Any]) -> tuple[str, str]:
    stored_code = str(doc.get("licenseCode") or "")
    if not stored_code:
        raise ValueError("License code is missing.")
    plain_code = plain_license_code(stored_code)
    fingerprint = str(doc.get("appFingerprint") or "").strip()
    if not fingerprint:
        raise ValueError("App fingerprint is missing.")
    encrypted = encrypt_license_payload(fingerprint, plain_code, build_license_payload(doc, plain_code))
    return plain_code, encrypted
