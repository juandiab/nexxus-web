from datetime import datetime
from typing import Any, Literal

from utils.time import ensure_utc_aware, utc_now

LicenseType = Literal["free", "trial", "enterprise", "enterprise_pro"]
UsageType = Literal["personal", "onprem", "cloud", "consulting"]
LicenseStatus = Literal["active", "expired", "expired_blocked", "deactivated"]

VALID_LICENSE_TYPES = frozenset({"free", "trial", "enterprise", "enterprise_pro"})
VALID_USAGE_TYPES = frozenset({"personal", "onprem", "cloud", "consulting"})

DEFAULT_VALIDITY_DAYS: dict[str, int] = {
    "free": 90,
    "trial": 30,
    "enterprise": 365,
    "enterprise_pro": 730,
}

FREE_ACTIVATION_VALIDITY_DAYS = 90
TRIAL_ACTIVATION_VALIDITY_DAYS = 30


def resolve_activation_terms(usage_type: str) -> tuple[str, int]:
    cleaned = usage_type.strip().lower()
    if cleaned not in VALID_USAGE_TYPES:
        raise ValueError(f"Invalid usage type: {usage_type}")
    if cleaned == "consulting":
        return "trial", TRIAL_ACTIVATION_VALIDITY_DAYS
    return "free", FREE_ACTIVATION_VALIDITY_DAYS


def usage_type_label(usage_type: str) -> str:
    labels = {
        "personal": "Personal",
        "onprem": "On-premises",
        "cloud": "Cloud",
        "consulting": "Consulting",
    }
    return labels.get(usage_type, usage_type)


def license_display_status(doc: dict[str, Any]) -> LicenseStatus:
    if doc.get("active") is False:
        return "deactivated"
    if doc.get("renewalBlocked"):
        return "expired_blocked"
    expiration = doc.get("expirationDate")
    if expiration is not None and ensure_utc_aware(expiration) <= utc_now():
        return "expired"
    return "active"


def serialize_license(doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "email": doc["email"],
        "country": doc.get("country", ""),
        "company": doc.get("company", ""),
        "registrationDate": doc.get("registrationDate"),
        "licenseType": doc.get("licenseType", "free"),
        "usageType": doc.get("usageType"),
        "application": doc.get("application", ""),
        "expirationDate": doc.get("expirationDate"),
        "validityDays": doc.get("validityDays"),
        "appFingerprint": doc.get("appFingerprint"),
        "appName": doc.get("appName"),
        "activationDate": doc.get("activationDate"),
        "hasLicenseCode": bool(doc.get("licenseCode")),
        "active": doc.get("active", True),
        "renewalBlocked": doc.get("renewalBlocked", False),
        "status": license_display_status(doc),
        "createdAt": doc.get("createdAt"),
        "updatedAt": doc.get("updatedAt"),
    }
