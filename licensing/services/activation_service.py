from __future__ import annotations

import secrets
import time
from datetime import datetime, timedelta, timezone
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.license import (
    FREE_ACTIVATION_VALIDITY_DAYS,
    serialize_license,
    resolve_activation_terms,
)
from services.license_service import generate_license_code
from services.offline_license_service import build_offline_license_package
from utils.time import utc_now

OTP_LENGTH = 6
OTP_EXPIRE_MINUTES = 15
OTP_EXPIRE_SECONDS = OTP_EXPIRE_MINUTES * 60
PENDING_COLLECTION = "activationPending"


def _generate_otp() -> str:
    return f"{secrets.randbelow(10**OTP_LENGTH):0{OTP_LENGTH}d}"


def normalize_otp(value: str) -> str:
    digits = "".join(ch for ch in value if ch.isdigit())
    if len(digits) != OTP_LENGTH:
        raise ValueError("Verification code must be exactly 6 digits.")
    return digits


def _otp_is_expired(pending: dict[str, Any]) -> bool:
    expires_unix = pending.get("otpExpiresAtUnix")
    if expires_unix is not None:
        return int(time.time()) >= int(expires_unix)
    return False


async def ensure_activation_pending_indexes(db: AsyncIOMotorDatabase) -> None:
    await db[PENDING_COLLECTION].create_index("expiresAt", expireAfterSeconds=0)
    await db[PENDING_COLLECTION].create_index(
        [("appFingerprint", 1), ("application", 1)],
        unique=True,
    )
    await db[PENDING_COLLECTION].create_index([("email", 1), ("application", 1)])


async def _assert_activation_available(
    db: AsyncIOMotorDatabase,
    *,
    app_fingerprint: str,
    application: str,
    email: str,
) -> None:
    existing = await db.licenses.find_one(
        {"appFingerprint": app_fingerprint, "application": application}
    )
    if existing is not None:
        raise ValueError("This deployment is already activated for this application")

    conflict = await db.licenses.find_one({"email": email, "application": application})
    if conflict is not None:
        raise ValueError("A license already exists for this email and application")


async def request_activation(
    db: AsyncIOMotorDatabase,
    *,
    app_fingerprint: str,
    app_name: str,
    activation_date: str,
    name: str,
    email: str,
    company: str,
    usage_type: str,
) -> tuple[dict[str, Any], str, str]:
    cleaned_email = email.strip().lower()
    cleaned_application = app_name.strip()
    cleaned_fingerprint = app_fingerprint.strip()
    if not cleaned_application:
        raise ValueError("App name is required")
    if not cleaned_fingerprint:
        raise ValueError("App fingerprint is required")

    license_type, validity_days = resolve_activation_terms(usage_type)
    cleaned_usage = usage_type.strip().lower()
    cleaned_company = company.strip()
    if cleaned_usage != "personal" and not cleaned_company:
        raise ValueError("Company is required for non-personal license use.")

    await _assert_activation_available(
        db,
        app_fingerprint=cleaned_fingerprint,
        application=cleaned_application,
        email=cleaned_email,
    )

    plain_code = generate_license_code()
    otp = _generate_otp()
    now_unix = int(time.time())
    expires_unix = now_unix + OTP_EXPIRE_SECONDS
    expires_at = datetime.fromtimestamp(expires_unix, tz=timezone.utc)
    now = utc_now()

    pending_doc = {
        "name": name.strip(),
        "email": cleaned_email,
        "company": cleaned_company,
        "application": cleaned_application,
        "appFingerprint": cleaned_fingerprint,
        "appName": cleaned_application,
        "activationDate": activation_date,
        "usageType": cleaned_usage,
        "licenseType": license_type,
        "validityDays": validity_days,
        "licenseCode": plain_code,
        "otp": otp,
        "otpExpiresAtUnix": expires_unix,
        "expiresAt": expires_at,
        "createdAt": now,
    }

    await db[PENDING_COLLECTION].update_one(
        {"appFingerprint": cleaned_fingerprint, "application": cleaned_application},
        {
            "$set": pending_doc,
            "$unset": {"otpHash": ""},
        },
        upsert=True,
    )

    preview = {
        "email": cleaned_email,
        "name": pending_doc["name"],
        "company": pending_doc["company"],
        "application": cleaned_application,
        "appFingerprint": cleaned_fingerprint,
        "appName": cleaned_application,
        "activationDate": activation_date,
        "usageType": cleaned_usage,
        "licenseType": license_type,
        "validityDays": validity_days,
        "otpExpiresAtUnix": expires_unix,
    }
    return preview, plain_code, otp


async def verify_activation_otp(
    db: AsyncIOMotorDatabase,
    *,
    app_fingerprint: str,
    app_name: str,
    email: str,
    otp: str,
) -> dict[str, Any]:
    cleaned_email = email.strip().lower()
    cleaned_application = app_name.strip()
    cleaned_fingerprint = app_fingerprint.strip()
    provided_otp = normalize_otp(otp)

    pending = await db[PENDING_COLLECTION].find_one(
        {
            "appFingerprint": cleaned_fingerprint,
            "application": cleaned_application,
        }
    )
    if pending is None:
        raise ValueError("No pending activation found. Request a new license code.")

    if pending.get("email") != cleaned_email:
        raise ValueError("Email does not match this activation request.")

    if _otp_is_expired(pending):
        await db[PENDING_COLLECTION].delete_one({"_id": pending["_id"]})
        raise ValueError("Verification code expired. Request a new license code.")

    stored_otp = str(pending.get("otp") or "")
    if not stored_otp or not secrets.compare_digest(stored_otp, provided_otp):
        raise ValueError("Invalid verification code. Use the 6-digit code from your email (not the license code).")

    await _assert_activation_available(
        db,
        app_fingerprint=cleaned_fingerprint,
        application=cleaned_application,
        email=cleaned_email,
    )

    registration_date = utc_now()
    validity_days = int(pending.get("validityDays", FREE_ACTIVATION_VALIDITY_DAYS))
    expiration_date = registration_date + timedelta(days=validity_days)
    now = utc_now()

    license_doc = {
        "name": pending["name"],
        "email": cleaned_email,
        "company": pending.get("company", ""),
        "usageType": pending.get("usageType"),
        "registrationDate": registration_date,
        "licenseType": pending.get("licenseType", "free"),
        "licenseCode": pending["licenseCode"],
        "application": cleaned_application,
        "expirationDate": expiration_date,
        "validityDays": validity_days,
        "appFingerprint": cleaned_fingerprint,
        "appName": cleaned_application,
        "activationDate": pending.get("activationDate"),
        "emailVerifiedAt": now,
        "active": True,
        "renewalBlocked": False,
        "renewalCount": 0,
        "createdAt": now,
        "updatedAt": now,
    }

    result = await db.licenses.insert_one(license_doc)
    await db[PENDING_COLLECTION].delete_one({"_id": pending["_id"]})

    license_doc["_id"] = result.inserted_id
    row = serialize_license(license_doc)
    row["appFingerprint"] = cleaned_fingerprint
    row["appName"] = cleaned_application
    row["activationDate"] = pending.get("activationDate")
    row["usageType"] = pending.get("usageType")
    row["offlineLicense"] = build_offline_license_package(license_doc)
    return row
