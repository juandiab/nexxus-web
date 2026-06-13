from __future__ import annotations

import logging
from typing import Any, Literal

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.license import license_display_status
from services.email_service import send_license_update_email
from services.license_payload import plain_license_code
from services.license_service import get_license_by_id

logger = logging.getLogger(__name__)

LicenseChangeKind = Literal[
    "extended",
    "type_changed",
    "updated",
    "expired",
    "deactivated",
    "reactivated",
]

_STATUS_LABELS = {
    "active": "Active",
    "expired": "Expired",
    "expired_blocked": "Expired (renewal blocked)",
    "deactivated": "Deactivated",
}


def _status_label(doc: dict[str, Any]) -> str:
    return _STATUS_LABELS.get(license_display_status(doc), "Active")


def _plain_code(doc: dict[str, Any]) -> str:
    stored = str(doc.get("licenseCode") or "").strip()
    if not stored:
        return ""
    return plain_license_code(stored)


async def notify_license_change(
    db: AsyncIOMotorDatabase,
    license_id: str,
    *,
    change: LicenseChangeKind,
    days_added: int | None = None,
) -> None:
    doc = await get_license_by_id(db, license_id)
    if doc is None:
        return

    email = str(doc.get("email") or "").strip().lower()
    if not email:
        logger.info("Skipping license update email for %s: no email on record", license_id)
        return

    application = str(doc.get("application") or doc.get("appName") or "your application")
    await send_license_update_email(
        to_address=email,
        name=str(doc.get("name") or ""),
        application=application,
        license_code=_plain_code(doc),
        license_type=str(doc.get("licenseType") or "free"),
        expiration_date=doc.get("expirationDate"),
        validity_days=doc.get("validityDays"),
        status_label=_status_label(doc),
        change=change,
        days_added=days_added,
    )


async def try_notify_license_change(
    db: AsyncIOMotorDatabase,
    license_id: str,
    *,
    change: LicenseChangeKind,
    days_added: int | None = None,
) -> None:
    try:
        await notify_license_change(
            db,
            license_id,
            change=change,
            days_added=days_added,
        )
    except Exception as exc:
        logger.warning(
            "License update email failed for %s (%s): %s",
            license_id,
            change,
            exc,
        )
