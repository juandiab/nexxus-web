import hashlib
import secrets
from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4

from db import get_database
from models.leads_api_key import LeadsApiKey, LeadsApiKeyCreate

COLLECTION = "leadsApiKeys"
_index_ready = False


class LeadsApiKeyNotFoundError(Exception):
    pass


class LeadsApiKeyLookupResult(str, Enum):
    OK = "ok"
    NOT_FOUND = "not_found"
    REVOKED = "revoked"
    FORBIDDEN = "forbidden"


def _now() -> datetime:
    return datetime.now(UTC)


def _hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def _key_prefix(api_key: str) -> str:
    return api_key[:8]


def generate_api_key() -> str:
    return f"nxlead_{secrets.token_urlsafe(32)}"


def _doc_to_key(doc: dict) -> LeadsApiKey:
    return LeadsApiKey(
        id=str(doc["_id"]),
        name=doc.get("name") or "",
        key_prefix=doc.get("key_prefix") or "",
        agent=doc.get("agent") or "leads",
        scopes=list(doc.get("scopes") or ["leads:write"]),
        created_by=doc.get("created_by") or "",
        created_at=doc.get("created_at"),
        last_used_at=doc.get("last_used_at"),
        revoked_at=doc.get("revoked_at"),
    )


async def _ensure_indexes() -> None:
    global _index_ready
    if _index_ready:
        return
    db = get_database()
    col = db[COLLECTION]
    await col.create_index("key_hash", unique=True)
    await col.create_index("revoked_at")
    await col.create_index("created_at")
    _index_ready = True


async def list_api_keys(*, include_revoked: bool = True) -> list[LeadsApiKey]:
    await _ensure_indexes()
    query: dict = {}
    if not include_revoked:
        query["revoked_at"] = None
    db = get_database()
    cursor = db[COLLECTION].find(query).sort("created_at", -1)
    keys: list[LeadsApiKey] = []
    async for doc in cursor:
        keys.append(_doc_to_key(doc))
    return keys


async def create_api_key(
    data: LeadsApiKeyCreate,
    *,
    created_by: str,
) -> tuple[str, LeadsApiKey]:
    await _ensure_indexes()
    raw_key = generate_api_key()
    now = _now()
    doc = {
        "_id": str(uuid4()),
        "name": data.name.strip(),
        "key_hash": _hash_api_key(raw_key),
        "key_prefix": _key_prefix(raw_key),
        "agent": data.agent,
        "scopes": data.scopes,
        "created_by": created_by,
        "created_at": now,
        "last_used_at": None,
        "revoked_at": None,
    }
    db = get_database()
    await db[COLLECTION].insert_one(doc)
    return raw_key, _doc_to_key(doc)


async def revoke_api_key(key_id: str) -> LeadsApiKey:
    await _ensure_indexes()
    db = get_database()
    existing = await db[COLLECTION].find_one({"_id": key_id})
    if not existing:
        raise LeadsApiKeyNotFoundError()
    if existing.get("revoked_at"):
        return _doc_to_key(existing)

    now = _now()
    await db[COLLECTION].update_one({"_id": key_id}, {"$set": {"revoked_at": now}})
    doc = await db[COLLECTION].find_one({"_id": key_id})
    return _doc_to_key(doc)


async def rotate_api_key(key_id: str, *, created_by: str) -> tuple[str, LeadsApiKey, LeadsApiKey]:
    await _ensure_indexes()
    db = get_database()
    existing = await db[COLLECTION].find_one({"_id": key_id})
    if not existing:
        raise LeadsApiKeyNotFoundError()

    revoked = await revoke_api_key(key_id)
    create = LeadsApiKeyCreate(
        name=existing.get("name") or "Rotated key",
        agent=existing.get("agent") or "leads",
        scopes=list(existing.get("scopes") or ["leads:write"]),
    )
    raw_key, new_key = await create_api_key(create, created_by=created_by)
    return raw_key, revoked, new_key


async def lookup_api_key(raw_key: str) -> tuple[LeadsApiKeyLookupResult, LeadsApiKey | None]:
    await _ensure_indexes()
    key = raw_key.strip()
    if not key:
        return LeadsApiKeyLookupResult.NOT_FOUND, None

    db = get_database()
    doc = await db[COLLECTION].find_one({"key_hash": _hash_api_key(key)})
    if not doc:
        return LeadsApiKeyLookupResult.NOT_FOUND, None

    if doc.get("revoked_at"):
        return LeadsApiKeyLookupResult.REVOKED, _doc_to_key(doc)

    scopes = list(doc.get("scopes") or [])
    if "leads:write" not in scopes:
        return LeadsApiKeyLookupResult.FORBIDDEN, _doc_to_key(doc)

    now = _now()
    await db[COLLECTION].update_one({"_id": doc["_id"]}, {"$set": {"last_used_at": now}})
    doc = await db[COLLECTION].find_one({"_id": doc["_id"]})
    return LeadsApiKeyLookupResult.OK, _doc_to_key(doc) if doc else None


async def validate_api_key(raw_key: str) -> LeadsApiKey | None:
    result, key = await lookup_api_key(raw_key)
    if result == LeadsApiKeyLookupResult.OK:
        return key
    return None


async def get_api_key(key_id: str) -> LeadsApiKey | None:
    await _ensure_indexes()
    db = get_database()
    doc = await db[COLLECTION].find_one({"_id": key_id})
    if not doc:
        return None
    return _doc_to_key(doc)
