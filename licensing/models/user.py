from typing import Any

VALID_ROLES = frozenset({"admin", "blog", "licensing", "user"})


def is_user_active(doc: dict[str, Any]) -> bool:
    return doc.get("active", True) is not False


def serialize_user(doc: dict[str, Any], *, passkey_count: int = 0) -> dict[str, Any]:
    must_change = bool(doc.get("mustChangePassword"))
    has_email = bool((doc.get("email") or "").strip())
    active = is_user_active(doc)
    setup_complete = active and not must_change and (passkey_count > 0 or not has_email)
    return {
        "id": str(doc["_id"]),
        "username": doc["username"],
        "displayName": doc.get("displayName", doc["username"]),
        "email": doc.get("email"),
        "role": doc.get("role", "user"),
        "active": active,
        "mustChangePassword": must_change,
        "passkeyRequired": passkey_count > 0,
        "passkeyCount": passkey_count,
        "setupComplete": setup_complete,
        "createdAt": doc.get("createdAt"),
    }
