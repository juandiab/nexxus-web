from __future__ import annotations

import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Literal

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.license import FREE_ACTIVATION_VALIDITY_DAYS
from services.license_payload import build_encrypted_license, format_utc, plain_license_code
from services.license_crypto import normalize_license_code
from services.license_service import find_license_by_code_and_app, rebind_license_to_deployment
from services.offline_license_service import find_license_by_deployment
from utils.time import ensure_utc_aware, utc_now


class SyncNotFoundError(Exception):
    pass


class SyncCodeMismatchError(Exception):
    pass


class SyncDeactivatedError(Exception):
    pass


class SyncExpiredError(Exception):
    def __init__(
        self,
        *,
        message: str,
        license_type: str,
        expiration_date: datetime | None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.license_type = license_type
        self.expiration_date = expiration_date


@dataclass
class SyncSuccess:
    status: Literal["active", "renewed"]
    message: str
    renewal_count: int
    license_type: str
    registration_date: datetime | None
    expiration_date: datetime | None
    validity_days: int
    encrypted_license: str


def _license_codes_match(stored: str, provided: str) -> bool:
    stored_plain = plain_license_code(stored)
    return secrets.compare_digest(
        normalize_license_code(stored_plain),
        normalize_license_code(provided),
    )


def _expired_message(license_type: str) -> str:
    if license_type == "trial":
        return "Trial expired. Request a new license or contact support."
    if license_type in {"enterprise", "enterprise_pro"}:
        return "License expired. Contact your administrator."
    if license_type == "free":
        return "License expired. Request a new license or contact support."
    return "License expired."


async def sync_license(
    db: AsyncIOMotorDatabase,
    *,
    app_fingerprint: str,
    app_name: str,
    license_code: str | None = None,
) -> SyncSuccess:
    cleaned_fingerprint = app_fingerprint.strip()
    cleaned_application = app_name.strip()
    if not cleaned_fingerprint or not cleaned_application:
        raise SyncNotFoundError()

    doc = await find_license_by_deployment(
        db,
        app_fingerprint=cleaned_fingerprint,
        app_name=cleaned_application,
    )
    if doc is None and license_code and license_code.strip():
        matched = await find_license_by_code_and_app(
            db,
            license_code=license_code,
            app_name=cleaned_application,
        )
        if matched is not None:
            doc = await rebind_license_to_deployment(
                db,
                matched,
                app_fingerprint=cleaned_fingerprint,
                app_name=cleaned_application,
            )
    if doc is None or not doc.get("licenseCode"):
        raise SyncNotFoundError()

    stored_code = str(doc["licenseCode"])
    plain_code = plain_license_code(stored_code)

    if license_code and license_code.strip():
        if not _license_codes_match(stored_code, license_code):
            raise SyncCodeMismatchError()

    if doc.get("active") is False:
        raise SyncDeactivatedError()

    now = utc_now()
    expiration = doc.get("expirationDate")
    expired = expiration is not None and ensure_utc_aware(expiration) <= now
    license_type = doc.get("licenseType", "free")
    status: Literal["active", "renewed"] = "active"
    message = ""
    sync_action = "sync"

    if expired:
        if license_type == "free" and not doc.get("renewalBlocked"):
            renewal_days = int(doc.get("validityDays") or FREE_ACTIVATION_VALIDITY_DAYS)
            new_expiration = now + timedelta(days=renewal_days)
            renewal_count = int(doc.get("renewalCount") or 0) + 1
            sync_action = "renewal"
            status = "renewed"
            message = f"Your free license was renewed until {format_utc(new_expiration)}."
            await db.licenses.update_one(
                {"_id": doc["_id"]},
                {
                    "$set": {
                        "registrationDate": now,
                        "expirationDate": new_expiration,
                        "renewalCount": renewal_count,
                        "lastSyncedAt": now,
                        "updatedAt": now,
                    },
                    "$push": {
                        "syncHistory": {
                            "at": now,
                            "action": sync_action,
                            "expirationDate": new_expiration,
                        }
                    },
                },
            )
            doc = await db.licenses.find_one({"_id": doc["_id"]}) or doc
        else:
            raise SyncExpiredError(
                message=_expired_message(license_type),
                license_type=license_type,
                expiration_date=ensure_utc_aware(expiration) if expiration else None,
            )
    else:
        await db.licenses.update_one(
            {"_id": doc["_id"]},
            {
                "$set": {
                    "lastSyncedAt": now,
                    "updatedAt": now,
                },
                "$push": {
                    "syncHistory": {
                        "at": now,
                        "action": sync_action,
                        "expirationDate": doc.get("expirationDate"),
                    }
                },
            },
        )

    _, encrypted = build_encrypted_license(doc)
    registration = doc.get("registrationDate")
    expiration = doc.get("expirationDate")
    return SyncSuccess(
        status=status,
        message=message,
        renewal_count=int(doc.get("renewalCount") or 0),
        license_type=str(doc.get("licenseType") or "free"),
        registration_date=ensure_utc_aware(registration) if registration else None,
        expiration_date=ensure_utc_aware(expiration) if expiration else None,
        validity_days=int(doc.get("validityDays") or 0),
        encrypted_license=encrypted,
    )
