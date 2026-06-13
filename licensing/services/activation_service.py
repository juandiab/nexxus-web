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
from services.license_service import (
    find_active_license_by_email_and_app,
    find_license_by_code_and_app,
    generate_license_code,
    rebind_license_to_deployment,
    _is_license_usable,
)
from services.license_payload import plain_license_code
from services.offline_license_service import (
    build_offline_license_package,
    find_license_by_deployment,
    find_verified_license_by_deployment,
)
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
) -> None:
    existing = await find_license_by_deployment(
        db,
        app_fingerprint=app_fingerprint,
        app_name=application,
    )
    if existing is not None:
        raise ValueError("This deployment is already activated for this application")


async def _build_activation_row(
    doc: dict[str, Any],
    *,
    app_fingerprint: str,
    app_name: str,
    message: str | None = None,
) -> dict[str, Any]:
    stored_code = str(doc.get("licenseCode") or "")
    if not stored_code:
        raise ValueError("No activated license found for this deployment")

    plain_code = plain_license_code(stored_code)
    row = serialize_license(doc)
    row["appFingerprint"] = app_fingerprint.strip()
    row["appName"] = app_name.strip()
    row["activationDate"] = doc.get("activationDate")
    row["usageType"] = doc.get("usageType")
    row["licenseCode"] = plain_code
    row["offlineLicense"] = build_offline_license_package(doc)
    if message:
        row["message"] = message
    return row


async def get_existing_deployment_activation(
    db: AsyncIOMotorDatabase,
    *,
    app_fingerprint: str,
    app_name: str,
    license_code: str | None = None,
    activation_date: str | None = None,
) -> dict[str, Any]:
    cleaned_fingerprint = app_fingerprint.strip()
    cleaned_application = app_name.strip()
    if not cleaned_application:
        raise ValueError("App name is required")
    if not cleaned_fingerprint:
        raise ValueError("App fingerprint is required")

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
                activation_date=activation_date,
            )

    if doc is None:
        raise ValueError("No activated license found for this deployment")

    return await _build_activation_row(
        doc,
        app_fingerprint=cleaned_fingerprint,
        app_name=cleaned_application,
    )


async def check_recoverable_license(
    db: AsyncIOMotorDatabase,
    *,
    email: str,
    app_name: str,
) -> dict[str, Any]:
    cleaned_email = email.strip().lower()
    cleaned_application = app_name.strip()
    if not cleaned_email:
        raise ValueError("Email is required")
    if not cleaned_application:
        raise ValueError("App name is required")

    doc = await find_active_license_by_email_and_app(
        db,
        email=cleaned_email,
        app_name=cleaned_application,
    )
    if doc is None:
        return {"found": False}

    return {
        "found": True,
        "email": cleaned_email,
        "application": cleaned_application,
        "name": doc.get("name", ""),
        "licenseType": doc.get("licenseType", "free"),
        "expirationDate": doc.get("expirationDate"),
    }


async def request_license_recovery(
    db: AsyncIOMotorDatabase,
    *,
    app_fingerprint: str,
    app_name: str,
    activation_date: str,
    email: str,
) -> tuple[dict[str, Any], str]:
    cleaned_email = email.strip().lower()
    cleaned_application = app_name.strip()
    cleaned_fingerprint = app_fingerprint.strip()
    if not cleaned_application:
        raise ValueError("App name is required")
    if not cleaned_fingerprint:
        raise ValueError("App fingerprint is required")

    existing = await find_license_by_deployment(
        db,
        app_fingerprint=cleaned_fingerprint,
        app_name=cleaned_application,
    )
    if existing is not None:
        raise ValueError("This deployment is already activated for this application")

    doc = await find_active_license_by_email_and_app(
        db,
        email=cleaned_email,
        app_name=cleaned_application,
    )
    if doc is None:
        raise ValueError("No active license found for this email and application.")

    otp = _generate_otp()
    now_unix = int(time.time())
    expires_unix = now_unix + OTP_EXPIRE_SECONDS
    expires_at = datetime.fromtimestamp(expires_unix, tz=timezone.utc)
    now = utc_now()

    pending_doc = {
        "intent": "recover",
        "licenseId": doc["_id"],
        "email": cleaned_email,
        "application": cleaned_application,
        "appFingerprint": cleaned_fingerprint,
        "appName": cleaned_application,
        "activationDate": activation_date,
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
        "application": cleaned_application,
        "name": doc.get("name", ""),
        "licenseType": doc.get("licenseType", "free"),
        "otpExpiresAtUnix": expires_unix,
    }
    return preview, otp


async def verify_license_recovery(
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
            "intent": "recover",
        }
    )
    if pending is None:
        raise ValueError("No pending recovery found. Request a new verification code.")

    if pending.get("email") != cleaned_email:
        raise ValueError("Email does not match this recovery request.")

    if _otp_is_expired(pending):
        await db[PENDING_COLLECTION].delete_one({"_id": pending["_id"]})
        raise ValueError("Verification code expired. Request a new code.")

    stored_otp = str(pending.get("otp") or "")
    if not stored_otp or not secrets.compare_digest(stored_otp, provided_otp):
        raise ValueError("Invalid verification code.")

    license_doc = await db.licenses.find_one({"_id": pending["licenseId"]})
    if license_doc is None or not _is_license_usable(license_doc):
        await db[PENDING_COLLECTION].delete_one({"_id": pending["_id"]})
        raise ValueError("The license for this recovery request is no longer available.")

    rebound = await rebind_license_to_deployment(
        db,
        license_doc,
        app_fingerprint=cleaned_fingerprint,
        app_name=cleaned_application,
        activation_date=pending.get("activationDate"),
    )
    await db[PENDING_COLLECTION].delete_one({"_id": pending["_id"]})

    return await _build_activation_row(
        rebound,
        app_fingerprint=cleaned_fingerprint,
        app_name=cleaned_application,
        message="License linked to this device.",
    )


async def request_activation(
    db: AsyncIOMotorDatabase,
    *,
    app_fingerprint: str,
    app_name: str,
    activation_date: str,
    name: str,
    email: str,
    company: str,
    country: str,
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
    cleaned_country = country.strip()
    if not cleaned_country:
        raise ValueError("Country is required.")
    if cleaned_usage != "personal" and not cleaned_company:
        raise ValueError("Company is required for non-personal license use.")

    await _assert_activation_available(
        db,
        app_fingerprint=cleaned_fingerprint,
        application=cleaned_application,
    )

    plain_code = generate_license_code()
    otp = _generate_otp()
    now_unix = int(time.time())
    expires_unix = now_unix + OTP_EXPIRE_SECONDS
    expires_at = datetime.fromtimestamp(expires_unix, tz=timezone.utc)
    now = utc_now()

    pending_doc = {
        "intent": "activate",
        "name": name.strip(),
        "email": cleaned_email,
        "company": cleaned_company,
        "country": cleaned_country,
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
            "intent": "activate",
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
    )

    registration_date = utc_now()
    validity_days = int(pending.get("validityDays", FREE_ACTIVATION_VALIDITY_DAYS))
    expiration_date = registration_date + timedelta(days=validity_days)
    now = utc_now()

    license_doc = {
        "name": pending["name"],
        "email": cleaned_email,
        "company": pending.get("company", ""),
        "country": pending.get("country", ""),
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
    return await _build_activation_row(
        license_doc,
        app_fingerprint=cleaned_fingerprint,
        app_name=cleaned_application,
    )
