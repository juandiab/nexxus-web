from __future__ import annotations

import secrets
import string
from datetime import timedelta
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from crypto import decrypt
from models.license import (
    FREE_ACTIVATION_VALIDITY_DAYS,
    DEFAULT_VALIDITY_DAYS,
    VALID_LICENSE_TYPES,
    serialize_license,
)
from utils.time import ensure_utc_aware, utc_now


def generate_license_code() -> str:
    alphabet = string.ascii_uppercase + string.digits
    segment = lambda: "".join(secrets.choice(alphabet) for _ in range(4))
    return f"{segment()}-{segment()}-{segment()}-{segment()}"


def _resolve_validity_days(license_type: str, validity_days: int | None) -> int:
    if validity_days is not None:
        return validity_days
    return DEFAULT_VALIDITY_DAYS.get(license_type, 30)


async def ensure_license_indexes(db: AsyncIOMotorDatabase) -> None:
    await db.licenses.create_index([("email", 1), ("application", 1)], unique=True)
    await db.licenses.create_index(
        [("appFingerprint", 1), ("application", 1)],
        unique=True,
        sparse=True,
    )
    await db.licenses.create_index("licenseType")
    await db.licenses.create_index("expirationDate")
    await db.licenses.create_index("registrationDate")


async def get_license_by_id(db: AsyncIOMotorDatabase, license_id: str) -> dict[str, Any] | None:
    try:
        oid = ObjectId(license_id)
    except Exception:
        return None
    return await db.licenses.find_one({"_id": oid})


async def list_licenses(db: AsyncIOMotorDatabase) -> list[dict[str, Any]]:
    docs = await db.licenses.find().sort("registrationDate", -1).to_list(length=None)
    return [serialize_license(doc) for doc in docs]


async def create_license(
    db: AsyncIOMotorDatabase,
    *,
    name: str,
    email: str,
    company: str,
    license_type: str,
    application: str,
    validity_days: int | None = None,
) -> tuple[dict[str, Any], str]:
    cleaned_type = license_type.strip().lower()
    if cleaned_type not in VALID_LICENSE_TYPES:
        raise ValueError(f"Invalid license type: {license_type}")

    cleaned_email = email.strip().lower()
    cleaned_application = application.strip()
    if not cleaned_application:
        raise ValueError("Application is required")

    existing = await db.licenses.find_one(
        {"email": cleaned_email, "application": cleaned_application}
    )
    if existing is not None:
        raise ValueError("A license already exists for this email and application")

    days = _resolve_validity_days(cleaned_type, validity_days)
    registration_date = utc_now()
    expiration_date = registration_date + timedelta(days=days)
    plain_code = generate_license_code()
    now = utc_now()

    doc = {
        "name": name.strip(),
        "email": cleaned_email,
        "company": company.strip(),
        "registrationDate": registration_date,
        "licenseType": cleaned_type,
        "licenseCode": plain_code,
        "application": cleaned_application,
        "expirationDate": expiration_date,
        "validityDays": days,
        "active": True,
        "renewalBlocked": False,
        "createdAt": now,
        "updatedAt": now,
    }
    result = await db.licenses.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_license(doc), plain_code


async def activate_license(
    db: AsyncIOMotorDatabase,
    *,
    app_fingerprint: str,
    app_name: str,
    activation_date: str,
    name: str,
    email: str,
    company: str,
) -> tuple[dict[str, Any], str]:
    cleaned_type = "free"
    cleaned_email = email.strip().lower()
    cleaned_application = app_name.strip()
    cleaned_fingerprint = app_fingerprint.strip()
    if not cleaned_application:
        raise ValueError("App name is required")
    if not cleaned_fingerprint:
        raise ValueError("App fingerprint is required")

    existing = await db.licenses.find_one(
        {"appFingerprint": cleaned_fingerprint, "application": cleaned_application}
    )
    if existing is not None:
        raise ValueError("This deployment is already activated for this application")

    conflict = await db.licenses.find_one(
        {"email": cleaned_email, "application": cleaned_application}
    )
    if conflict is not None:
        raise ValueError("A license already exists for this email and application")

    days = FREE_ACTIVATION_VALIDITY_DAYS
    registration_date = utc_now()
    expiration_date = registration_date + timedelta(days=days)
    plain_code = generate_license_code()
    now = utc_now()

    doc = {
        "name": name.strip(),
        "email": cleaned_email,
        "company": company.strip(),
        "registrationDate": registration_date,
        "licenseType": cleaned_type,
        "licenseCode": plain_code,
        "application": cleaned_application,
        "expirationDate": expiration_date,
        "validityDays": days,
        "appFingerprint": cleaned_fingerprint,
        "appName": cleaned_application,
        "activationDate": activation_date,
        "active": True,
        "renewalBlocked": False,
        "createdAt": now,
        "updatedAt": now,
    }
    result = await db.licenses.insert_one(doc)
    doc["_id"] = result.inserted_id
    row = serialize_license(doc)
    row["appFingerprint"] = cleaned_fingerprint
    row["appName"] = cleaned_application
    row["activationDate"] = activation_date
    return row, plain_code


async def delete_license_by_fingerprint(
    db: AsyncIOMotorDatabase,
    *,
    app_fingerprint: str,
    application: str,
) -> bool:
    result = await db.licenses.delete_one(
        {"appFingerprint": app_fingerprint.strip(), "application": application.strip()}
    )
    return result.deleted_count > 0


async def update_license(
    db: AsyncIOMotorDatabase,
    license_id: str,
    *,
    name: str,
    email: str,
    company: str,
    license_type: str,
    application: str,
    validity_days: int,
) -> dict[str, Any] | None:
    doc = await get_license_by_id(db, license_id)
    if doc is None:
        return None

    cleaned_type = license_type.strip().lower()
    if cleaned_type not in VALID_LICENSE_TYPES:
        raise ValueError(f"Invalid license type: {license_type}")

    cleaned_email = email.strip().lower()
    cleaned_application = application.strip()
    if not cleaned_application:
        raise ValueError("Application is required")

    conflict = await db.licenses.find_one(
        {
            "email": cleaned_email,
            "application": cleaned_application,
            "_id": {"$ne": doc["_id"]},
        }
    )
    if conflict is not None:
        raise ValueError("A license already exists for this email and application")

    registration_date = doc.get("registrationDate") or doc.get("createdAt") or utc_now()
    expiration_date = registration_date + timedelta(days=validity_days)

    await db.licenses.update_one(
        {"_id": doc["_id"]},
        {
            "$set": {
                "name": name.strip(),
                "email": cleaned_email,
                "company": company.strip(),
                "licenseType": cleaned_type,
                "application": cleaned_application,
                "validityDays": validity_days,
                "expirationDate": expiration_date,
                "updatedAt": utc_now(),
            }
        },
    )
    updated = await get_license_by_id(db, license_id)
    if updated is None:
        return None
    return serialize_license(updated)


async def delete_license(db: AsyncIOMotorDatabase, license_id: str) -> bool:
    doc = await get_license_by_id(db, license_id)
    if doc is None:
        return False
    result = await db.licenses.delete_one({"_id": doc["_id"]})
    return result.deleted_count > 0


def _append_admin_history(doc: dict[str, Any], action: str, *, note: str = "") -> dict[str, Any]:
    entry: dict[str, Any] = {"at": utc_now(), "action": action}
    if note:
        entry["note"] = note
    return entry


async def expire_license(db: AsyncIOMotorDatabase, license_id: str) -> dict[str, Any] | None:
    doc = await get_license_by_id(db, license_id)
    if doc is None:
        return None

    now = utc_now()
    history_entry = _append_admin_history(doc, "expire", note="Admin forced expiration")
    await db.licenses.update_one(
        {"_id": doc["_id"]},
        {
            "$set": {
                "expirationDate": now - timedelta(seconds=1),
                "renewalBlocked": True,
                "updatedAt": now,
            },
            "$push": {"adminHistory": history_entry},
        },
    )
    updated = await get_license_by_id(db, license_id)
    return serialize_license(updated) if updated else None


async def set_license_active(
    db: AsyncIOMotorDatabase,
    license_id: str,
    *,
    active: bool,
) -> dict[str, Any] | None:
    doc = await get_license_by_id(db, license_id)
    if doc is None:
        return None

    now = utc_now()
    action = "reactivate" if active else "deactivate"
    history_entry = _append_admin_history(doc, action)
    await db.licenses.update_one(
        {"_id": doc["_id"]},
        {
            "$set": {
                "active": active,
                "updatedAt": now,
            },
            "$push": {"adminHistory": history_entry},
        },
    )
    updated = await get_license_by_id(db, license_id)
    return serialize_license(updated) if updated else None


async def extend_license(
    db: AsyncIOMotorDatabase,
    license_id: str,
    *,
    days: int,
) -> dict[str, Any] | None:
    doc = await get_license_by_id(db, license_id)
    if doc is None:
        return None

    now = utc_now()
    current_expiration = doc.get("expirationDate")
    base = now
    if current_expiration is not None:
        aware = ensure_utc_aware(current_expiration)
        if aware > base:
            base = aware

    new_expiration = base + timedelta(days=days)
    history_entry = _append_admin_history(doc, "extend", note=f"+{days} days")
    await db.licenses.update_one(
        {"_id": doc["_id"]},
        {
            "$set": {
                "expirationDate": new_expiration,
                "validityDays": int(doc.get("validityDays") or days) + days,
                "renewalBlocked": False,
                "updatedAt": now,
            },
            "$push": {"adminHistory": history_entry},
        },
    )
    updated = await get_license_by_id(db, license_id)
    return serialize_license(updated) if updated else None


async def change_license_type(
    db: AsyncIOMotorDatabase,
    license_id: str,
    *,
    license_type: str,
    recalculate_validity: bool = True,
) -> dict[str, Any] | None:
    doc = await get_license_by_id(db, license_id)
    if doc is None:
        return None

    cleaned_type = license_type.strip().lower()
    if cleaned_type not in VALID_LICENSE_TYPES:
        raise ValueError(f"Invalid license type: {license_type}")

    now = utc_now()
    updates: dict[str, Any] = {
        "licenseType": cleaned_type,
        "updatedAt": now,
    }
    if recalculate_validity:
        days = DEFAULT_VALIDITY_DAYS.get(cleaned_type, 30)
        registration_date = doc.get("registrationDate") or doc.get("createdAt") or now
        updates["validityDays"] = days
        updates["expirationDate"] = ensure_utc_aware(registration_date) + timedelta(days=days)

    history_entry = _append_admin_history(doc, "change_type", note=cleaned_type)
    await db.licenses.update_one(
        {"_id": doc["_id"]},
        {
            "$set": updates,
            "$push": {"adminHistory": history_entry},
        },
    )
    updated = await get_license_by_id(db, license_id)
    return serialize_license(updated) if updated else None


async def verify_license_code(
    db: AsyncIOMotorDatabase,
    *,
    email: str,
    application: str,
    license_code: str,
) -> dict[str, Any] | None:
    cleaned_email = email.strip().lower()
    cleaned_application = application.strip()
    doc = await db.licenses.find_one(
        {"email": cleaned_email, "application": cleaned_application}
    )
    if doc is None or not doc.get("licenseCode"):
        return None

    provided = license_code.strip().upper()
    stored = doc["licenseCode"]
    matched = False
    try:
        matched = secrets.compare_digest(decrypt(stored), provided)
    except ValueError:
        matched = secrets.compare_digest(str(stored).strip().upper(), provided)
    if not matched:
        return None

    expiration = doc.get("expirationDate")
    if expiration is not None and ensure_utc_aware(expiration) < utc_now():
        return None

    if doc.get("active") is False:
        return None

    return serialize_license(doc)
