from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from services.license_payload import build_encrypted_license

OFFLINE_LICENSE_FORMAT = "nexxus-offline-license"
OFFLINE_LICENSE_VERSION = 1
OFFLINE_LICENSE_ALGORITHM = "AES-256-GCM+HKDF-SHA256"
OFFLINE_LICENSE_EXTENSION = ".lic"


def offline_license_filename(app_name: str, exported_at: datetime | str | None = None) -> str:
    safe_name = "".join(ch for ch in app_name.strip() if ch.isalnum() or ch in "-_") or "app"
    when = datetime.now(timezone.utc)
    if exported_at:
        if isinstance(exported_at, str):
            when = datetime.fromisoformat(exported_at.replace("Z", "+00:00"))
        else:
            when = exported_at
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    date_part = when.astimezone(timezone.utc).strftime("%d%m%Y")
    return f"{safe_name}_app_{date_part}{OFFLINE_LICENSE_EXTENSION}"


def build_offline_license_package(doc: dict[str, Any]) -> dict[str, Any]:
    plain_code, encrypted = build_encrypted_license(doc)
    fingerprint = str(doc.get("appFingerprint") or "").strip()
    app_name = str(doc.get("appName") or doc.get("application") or "").strip()
    return {
        "format": OFFLINE_LICENSE_FORMAT,
        "version": OFFLINE_LICENSE_VERSION,
        "algorithm": OFFLINE_LICENSE_ALGORITHM,
        "appFingerprint": fingerprint,
        "appName": app_name,
        "licenseCode": plain_code,
        "encryptedLicense": encrypted,
        "exportedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


async def find_verified_license(
    db: AsyncIOMotorDatabase,
    *,
    app_fingerprint: str,
    app_name: str,
    email: str,
) -> dict[str, Any] | None:
    cleaned_fingerprint = app_fingerprint.strip()
    cleaned_application = app_name.strip()
    cleaned_email = email.strip().lower()
    if not cleaned_fingerprint or not cleaned_application or not cleaned_email:
        return None

    return await db.licenses.find_one(
        {
            "appFingerprint": cleaned_fingerprint,
            "application": cleaned_application,
            "email": cleaned_email,
            "emailVerifiedAt": {"$exists": True},
        }
    )


async def get_offline_license_package(
    db: AsyncIOMotorDatabase,
    *,
    app_fingerprint: str,
    app_name: str,
    email: str,
) -> dict[str, Any]:
    doc = await find_verified_license(
        db,
        app_fingerprint=app_fingerprint,
        app_name=app_name,
        email=email,
    )
    if doc is None:
        raise ValueError("No verified license found for this deployment.")
    return build_offline_license_package(doc)
