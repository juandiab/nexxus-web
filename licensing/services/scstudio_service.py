from __future__ import annotations

import hashlib
import secrets
import uuid
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.license import serialize_license
from crypto import decrypt, encrypt
from services.scstudio_crypto import encrypt_scstudio_database
from utils.time import utc_now

SERVERS_COLLECTION = "scstudioServers"
API_KEYS_COLLECTION = "scstudioApiKeys"


class ScStudioRegistrationConflictError(Exception):
    pass


class ScStudioNotFoundError(Exception):
    pass


class ScStudioInvalidStateError(Exception):
    pass


class ScStudioApiKeyNotFoundError(Exception):
    pass


class ScStudioApiKeyUnavailableError(Exception):
    pass


def _hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def _key_prefix(api_key: str) -> str:
    return api_key[:8]


def _generate_api_key() -> str:
    return secrets.token_urlsafe(32)


def _serialize_server(doc: dict[str, Any], *, key_doc: dict[str, Any] | None = None) -> dict[str, Any]:
    row = {
        "id": str(doc["_id"]),
        "serverName": doc["serverName"],
        "serverFingerprint": doc["serverFingerprint"],
        "ipAddress": doc["ipAddress"],
        "publicIpAddress": doc["publicIpAddress"],
        "status": doc["status"],
        "serverId": doc.get("serverId"),
        "approvedAt": doc.get("approvedAt"),
        "approvedBy": doc.get("approvedBy"),
        "rejectedAt": doc.get("rejectedAt"),
        "lastSyncAt": doc.get("lastSyncAt"),
        "createdAt": doc.get("createdAt"),
        "updatedAt": doc.get("updatedAt"),
        "apiKeyId": None,
        "keyPrefix": None,
        "apiKeyActive": None,
        "apiKeyRetrievable": False,
        "apiKeyLastUsedAt": None,
    }
    if key_doc is not None:
        row.update(
            {
                "apiKeyId": str(key_doc["_id"]),
                "keyPrefix": key_doc["keyPrefix"],
                "apiKeyActive": key_doc.get("active", True),
                "apiKeyRetrievable": bool(key_doc.get("keyEncrypted")),
                "apiKeyLastUsedAt": key_doc.get("lastUsedAt"),
            }
        )
    return row


def _serialize_api_key(doc: dict[str, Any], *, server_name: str = "") -> dict[str, Any]:
    return {
        "id": str(doc["_id"]),
        "serverId": doc["serverId"],
        "serverName": server_name,
        "keyPrefix": doc["keyPrefix"],
        "active": doc.get("active", True),
        "retrievable": bool(doc.get("keyEncrypted")),
        "createdAt": doc.get("createdAt"),
        "lastUsedAt": doc.get("lastUsedAt"),
        "createdBy": doc.get("createdBy"),
    }


async def _dedupe_api_keys_by_server(db: AsyncIOMotorDatabase) -> None:
    keys = await db[API_KEYS_COLLECTION].find().sort("createdAt", -1).to_list(length=None)
    seen_server_ids: set[str] = set()
    for key in keys:
        server_id = key.get("serverId")
        if not server_id:
            continue
        if server_id in seen_server_ids:
            await db[API_KEYS_COLLECTION].delete_one({"_id": key["_id"]})
        else:
            seen_server_ids.add(server_id)


async def ensure_scstudio_indexes(db: AsyncIOMotorDatabase) -> None:
    await db[SERVERS_COLLECTION].create_index("serverFingerprint", unique=True)
    await db[SERVERS_COLLECTION].create_index("serverId", unique=True, sparse=True)
    await db[SERVERS_COLLECTION].create_index("status")
    await _dedupe_api_keys_by_server(db)
    index_info = await db[API_KEYS_COLLECTION].index_information()
    server_id_index = index_info.get("serverId_1")
    if server_id_index and not server_id_index.get("unique"):
        await db[API_KEYS_COLLECTION].drop_index("serverId_1")
    await db[API_KEYS_COLLECTION].create_index("keyHash", unique=True)
    await db[API_KEYS_COLLECTION].create_index("serverId", unique=True)
    await db[API_KEYS_COLLECTION].create_index([("serverId", 1), ("active", 1)])


async def _get_api_key_for_server_id(
    db: AsyncIOMotorDatabase,
    server_id: str | None,
) -> dict[str, Any] | None:
    if not server_id:
        return None
    return await db[API_KEYS_COLLECTION].find_one({"serverId": server_id.strip()})


async def register_server(
    db: AsyncIOMotorDatabase,
    *,
    server_name: str,
    server_fingerprint: str,
    ip_address: str,
    public_ip_address: str,
) -> dict[str, Any]:
    cleaned_fingerprint = server_fingerprint.strip()
    now = utc_now()
    existing = await db[SERVERS_COLLECTION].find_one({"serverFingerprint": cleaned_fingerprint})

    if existing is not None:
        if existing.get("status") == "approved":
            raise ScStudioRegistrationConflictError()
        updates = {
            "serverName": server_name.strip(),
            "ipAddress": ip_address.strip(),
            "publicIpAddress": public_ip_address.strip(),
            "status": "pending",
            "rejectedAt": None,
            "updatedAt": now,
        }
        await db[SERVERS_COLLECTION].update_one({"_id": existing["_id"]}, {"$set": updates})
        updated = await db[SERVERS_COLLECTION].find_one({"_id": existing["_id"]})
        assert updated is not None
        key_doc = await _get_api_key_for_server_id(db, updated.get("serverId"))
        return _serialize_server(updated, key_doc=key_doc)

    doc = {
        "serverName": server_name.strip(),
        "serverFingerprint": cleaned_fingerprint,
        "ipAddress": ip_address.strip(),
        "publicIpAddress": public_ip_address.strip(),
        "status": "pending",
        "serverId": None,
        "approvedAt": None,
        "approvedBy": None,
        "rejectedAt": None,
        "lastSyncAt": None,
        "createdAt": now,
        "updatedAt": now,
    }
    result = await db[SERVERS_COLLECTION].insert_one(doc)
    created = await db[SERVERS_COLLECTION].find_one({"_id": result.inserted_id})
    assert created is not None
    return _serialize_server(created)


async def list_servers(db: AsyncIOMotorDatabase) -> list[dict[str, Any]]:
    docs = await db[SERVERS_COLLECTION].find().sort("createdAt", -1).to_list(length=None)
    rows: list[dict[str, Any]] = []
    for doc in docs:
        key_doc = await _get_api_key_for_server_id(db, doc.get("serverId"))
        rows.append(_serialize_server(doc, key_doc=key_doc))
    return rows


async def get_server_by_id(db: AsyncIOMotorDatabase, registration_id: str) -> dict[str, Any] | None:
    try:
        oid = ObjectId(registration_id)
    except Exception:
        return None
    doc = await db[SERVERS_COLLECTION].find_one({"_id": oid})
    if doc is None:
        return None
    key_doc = await _get_api_key_for_server_id(db, doc.get("serverId"))
    return _serialize_server(doc, key_doc=key_doc)


async def get_server_doc_by_server_id(
    db: AsyncIOMotorDatabase,
    server_id: str,
) -> dict[str, Any] | None:
    return await db[SERVERS_COLLECTION].find_one({"serverId": server_id.strip()})


async def _create_api_key_record(
    db: AsyncIOMotorDatabase,
    *,
    server_id: str,
    created_by: str,
) -> tuple[str, dict[str, Any]]:
    api_key = _generate_api_key()
    now = utc_now()
    doc = {
        "serverId": server_id,
        "keyHash": _hash_api_key(api_key),
        "keyPrefix": _key_prefix(api_key),
        "keyEncrypted": encrypt(api_key),
        "active": True,
        "createdAt": now,
        "lastUsedAt": None,
        "createdBy": created_by,
    }
    result = await db[API_KEYS_COLLECTION].insert_one(doc)
    created = await db[API_KEYS_COLLECTION].find_one({"_id": result.inserted_id})
    assert created is not None
    return api_key, created


async def approve_server(
    db: AsyncIOMotorDatabase,
    registration_id: str,
    *,
    approved_by: str,
) -> tuple[dict[str, Any], str]:
    try:
        oid = ObjectId(registration_id)
    except Exception:
        raise ScStudioNotFoundError() from None

    doc = await db[SERVERS_COLLECTION].find_one({"_id": oid})
    if doc is None:
        raise ScStudioNotFoundError()
    if doc.get("status") == "approved":
        raise ScStudioInvalidStateError("Server is already approved.")
    if doc.get("status") == "rejected":
        raise ScStudioInvalidStateError("Rejected registration must re-register before approval.")

    server_id = str(uuid.uuid4())
    now = utc_now()
    await db[SERVERS_COLLECTION].update_one(
        {"_id": oid},
        {
            "$set": {
                "status": "approved",
                "serverId": server_id,
                "approvedAt": now,
                "approvedBy": approved_by,
                "rejectedAt": None,
                "updatedAt": now,
            }
        },
    )

    api_key, _ = await _create_api_key_record(
        db,
        server_id=server_id,
        created_by=approved_by,
    )

    updated = await db[SERVERS_COLLECTION].find_one({"_id": oid})
    assert updated is not None
    key_doc = await db[API_KEYS_COLLECTION].find_one({"serverId": server_id})
    return _serialize_server(updated, key_doc=key_doc), api_key


async def reject_server(db: AsyncIOMotorDatabase, registration_id: str) -> dict[str, Any]:
    try:
        oid = ObjectId(registration_id)
    except Exception:
        raise ScStudioNotFoundError() from None

    doc = await db[SERVERS_COLLECTION].find_one({"_id": oid})
    if doc is None:
        raise ScStudioNotFoundError()
    if doc.get("status") == "approved":
        raise ScStudioInvalidStateError("Cannot reject an approved server.")

    now = utc_now()
    await db[SERVERS_COLLECTION].update_one(
        {"_id": oid},
        {
            "$set": {
                "status": "rejected",
                "rejectedAt": now,
                "updatedAt": now,
            }
        },
    )
    updated = await db[SERVERS_COLLECTION].find_one({"_id": oid})
    assert updated is not None
    key_doc = await _get_api_key_for_server_id(db, updated.get("serverId"))
    return _serialize_server(updated, key_doc=key_doc)


async def validate_api_key(
    db: AsyncIOMotorDatabase,
    *,
    api_key: str,
    server_id: str,
) -> dict[str, Any]:
    key_hash = _hash_api_key(api_key.strip())
    key_doc = await db[API_KEYS_COLLECTION].find_one({"keyHash": key_hash, "active": True})
    if key_doc is None:
        raise ScStudioInvalidStateError("Invalid or disabled API key.")

    if key_doc.get("serverId") != server_id.strip():
        raise ScStudioInvalidStateError("API key does not match the requested server.")

    server_doc = await get_server_doc_by_server_id(db, server_id)
    if server_doc is None or server_doc.get("status") != "approved":
        raise ScStudioInvalidStateError("Server is not approved.")

    now = utc_now()
    await db[API_KEYS_COLLECTION].update_one(
        {"_id": key_doc["_id"]},
        {"$set": {"lastUsedAt": now}},
    )

    return {
        "serverId": server_doc["serverId"],
        "serverName": server_doc["serverName"],
        "serverFingerprint": server_doc["serverFingerprint"],
        "registrationId": str(server_doc["_id"]),
    }


async def export_licenses_for_sync(db: AsyncIOMotorDatabase) -> list[dict[str, Any]]:
    docs = await db.licenses.find().sort("registrationDate", -1).to_list(length=None)
    return [serialize_license(doc) for doc in docs]


async def sync_license_database(
    db: AsyncIOMotorDatabase,
    *,
    server_fingerprint: str,
    server_id: str,
) -> dict[str, Any]:
    licenses = await export_licenses_for_sync(db)
    now = utc_now()
    payload = {
        "version": 1,
        "exportedAt": now.isoformat(),
        "licenseCount": len(licenses),
        "licenses": licenses,
    }
    encrypted = encrypt_scstudio_database(server_fingerprint, payload)

    await db[SERVERS_COLLECTION].update_one(
        {"serverId": server_id},
        {"$set": {"lastSyncAt": now, "updatedAt": now}},
    )

    return {
        "serverId": server_id,
        "licenseCount": len(licenses),
        "syncedAt": now,
        "encryptedDatabase": encrypted,
    }


async def list_api_keys(db: AsyncIOMotorDatabase) -> list[dict[str, Any]]:
    keys = await db[API_KEYS_COLLECTION].find().sort("createdAt", -1).to_list(length=None)
    server_ids = {key["serverId"] for key in keys}
    server_names: dict[str, str] = {}
    if server_ids:
        async for server in db[SERVERS_COLLECTION].find({"serverId": {"$in": list(server_ids)}}):
            if server.get("serverId"):
                server_names[server["serverId"]] = server.get("serverName", "")

    return [
        _serialize_api_key(key, server_name=server_names.get(key["serverId"], ""))
        for key in keys
    ]


async def regenerate_api_key(
    db: AsyncIOMotorDatabase,
    registration_id: str,
    *,
    created_by: str,
) -> tuple[str, dict[str, Any]]:
    try:
        oid = ObjectId(registration_id)
    except Exception:
        raise ScStudioNotFoundError() from None

    doc = await db[SERVERS_COLLECTION].find_one({"_id": oid})
    if doc is None:
        raise ScStudioNotFoundError()
    if doc.get("status") != "approved" or not doc.get("serverId"):
        raise ScStudioInvalidStateError("Server must be approved before regenerating an API key.")

    server_id = str(doc["serverId"])
    await db[API_KEYS_COLLECTION].delete_many({"serverId": server_id})

    api_key, key_doc = await _create_api_key_record(
        db,
        server_id=server_id,
        created_by=created_by,
    )
    return api_key, _serialize_server(doc, key_doc=key_doc)


async def create_api_key(
    db: AsyncIOMotorDatabase,
    *,
    server_id: str,
    created_by: str,
) -> tuple[str, dict[str, Any]]:
    server_doc = await get_server_doc_by_server_id(db, server_id)
    if server_doc is None or server_doc.get("status") != "approved":
        raise ScStudioInvalidStateError("Server not found or not approved.")

    existing = await _get_api_key_for_server_id(db, server_id)
    if existing is not None:
        raise ScStudioInvalidStateError(
            "This server already has an API key. Regenerate it instead of creating another."
        )

    api_key, key_doc = await _create_api_key_record(
        db,
        server_id=server_id.strip(),
        created_by=created_by,
    )
    return api_key, _serialize_api_key(
        key_doc,
        server_name=server_doc.get("serverName", ""),
    )


async def set_api_key_active(
    db: AsyncIOMotorDatabase,
    key_id: str,
    *,
    active: bool,
) -> dict[str, Any]:
    try:
        oid = ObjectId(key_id)
    except Exception:
        raise ScStudioApiKeyNotFoundError() from None

    doc = await db[API_KEYS_COLLECTION].find_one({"_id": oid})
    if doc is None:
        raise ScStudioApiKeyNotFoundError()

    await db[API_KEYS_COLLECTION].update_one({"_id": oid}, {"$set": {"active": active}})

    server_doc = await get_server_doc_by_server_id(db, doc["serverId"])
    server_name = server_doc.get("serverName", "") if server_doc else ""
    updated = await db[API_KEYS_COLLECTION].find_one({"_id": oid})
    assert updated is not None
    return _serialize_api_key(updated, server_name=server_name)


async def get_api_key_secret(db: AsyncIOMotorDatabase, key_id: str) -> dict[str, Any]:
    try:
        oid = ObjectId(key_id)
    except Exception:
        raise ScStudioApiKeyNotFoundError() from None

    doc = await db[API_KEYS_COLLECTION].find_one({"_id": oid})
    if doc is None:
        raise ScStudioApiKeyNotFoundError()

    encrypted = doc.get("keyEncrypted")
    if not encrypted:
        raise ScStudioApiKeyUnavailableError(
            "This API key was created before secure storage was enabled. Create a new key."
        )

    try:
        api_key = decrypt(str(encrypted))
    except ValueError as exc:
        raise ScStudioApiKeyUnavailableError("Unable to decrypt API key.") from exc

    server_doc = await get_server_doc_by_server_id(db, doc["serverId"])
    server_name = server_doc.get("serverName", "") if server_doc else ""

    return {
        "id": str(doc["_id"]),
        "serverId": doc["serverId"],
        "serverName": server_name,
        "keyPrefix": doc["keyPrefix"],
        "apiKey": api_key,
    }


async def delete_api_key(db: AsyncIOMotorDatabase, key_id: str) -> None:
    try:
        oid = ObjectId(key_id)
    except Exception:
        raise ScStudioApiKeyNotFoundError() from None

    result = await db[API_KEYS_COLLECTION].delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise ScStudioApiKeyNotFoundError()


async def delete_server(db: AsyncIOMotorDatabase, registration_id: str) -> None:
    try:
        oid = ObjectId(registration_id)
    except Exception:
        raise ScStudioNotFoundError() from None

    doc = await db[SERVERS_COLLECTION].find_one({"_id": oid})
    if doc is None:
        raise ScStudioNotFoundError()

    server_id = doc.get("serverId")
    if server_id:
        await db[API_KEYS_COLLECTION].delete_many({"serverId": server_id})

    result = await db[SERVERS_COLLECTION].delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise ScStudioNotFoundError()
