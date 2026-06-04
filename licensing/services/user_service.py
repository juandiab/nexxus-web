from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from config import settings
from models.user import VALID_ROLES, serialize_user
from services.auth_service import hash_password, verify_password
from utils.time import utc_now


async def ensure_default_admin(db: AsyncIOMotorDatabase) -> None:
    cleaned_username = settings.admin_console_user.strip().lower()
    existing = await db.users.find_one({"username": cleaned_username})
    if existing is not None:
        updates: dict[str, Any] = {"updatedAt": utc_now()}
        if not existing.get("role"):
            updates["role"] = "admin"
        if not existing.get("hashedPassword"):
            updates["hashedPassword"] = hash_password(settings.admin_console_password)
        if len(updates) > 1:
            await db.users.update_one({"_id": existing["_id"]}, {"$set": updates})
        return

    await db.users.insert_one(
        {
            "username": cleaned_username,
            "displayName": cleaned_username.title(),
            "email": None,
            "role": "admin",
            "hashedPassword": hash_password(settings.admin_console_password),
            "mustChangePassword": False,
            "active": True,
            "createdAt": utc_now(),
            "updatedAt": utc_now(),
        }
    )


async def ensure_user_indexes(db: AsyncIOMotorDatabase) -> None:
    await db.users.create_index("username", unique=True)
    await db.users.create_index("email", unique=True, sparse=True)


async def get_user_by_username(db: AsyncIOMotorDatabase, username: str) -> dict | None:
    return await db.users.find_one({"username": username.strip().lower()})


async def get_user_by_email(db: AsyncIOMotorDatabase, email: str) -> dict | None:
    cleaned = email.strip().lower()
    if not cleaned:
        return None
    return await db.users.find_one({"email": cleaned})


async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str) -> dict | None:
    try:
        oid = ObjectId(user_id)
    except Exception:
        return None
    return await db.users.find_one({"_id": oid})


async def list_users(db: AsyncIOMotorDatabase) -> list[dict[str, Any]]:
    users = await db.users.find().sort("username", 1).to_list(length=None)
    rows: list[dict[str, Any]] = []
    for user in users:
        count = await db.passkeys.count_documents({"userId": user["_id"]})
        rows.append(serialize_user(user, passkey_count=count))
    return rows


async def create_user(
    db: AsyncIOMotorDatabase,
    *,
    username: str,
    display_name: str,
    email: str,
    password: str,
    role: str = "user",
    must_change_password: bool = True,
) -> dict[str, Any]:
    cleaned_username = username.strip().lower()
    if await get_user_by_username(db, cleaned_username):
        raise ValueError(f"Username '{cleaned_username}' already exists")

    cleaned_email = email.strip().lower()
    if await get_user_by_email(db, cleaned_email):
        raise ValueError(f"Email '{cleaned_email}' is already in use")

    cleaned_role = role.strip().lower()
    if cleaned_role not in VALID_ROLES:
        raise ValueError(f"Invalid role '{role}'")

    cleaned_password = password.strip()
    if len(cleaned_password) < 8:
        raise ValueError("Password must be at least 8 characters")

    doc = {
        "username": cleaned_username,
        "displayName": display_name.strip(),
        "email": cleaned_email,
        "role": cleaned_role,
        "hashedPassword": hash_password(cleaned_password),
        "mustChangePassword": must_change_password,
        "active": True,
        "createdAt": utc_now(),
        "updatedAt": utc_now(),
    }
    result = await db.users.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_user(doc, passkey_count=0)


async def change_password(
    db: AsyncIOMotorDatabase,
    user: dict[str, Any],
    *,
    current_password: str,
    new_password: str,
) -> None:
    hashed = user.get("hashedPassword")
    if not hashed or not verify_password(current_password, hashed):
        raise ValueError("Current password is incorrect")

    cleaned = new_password.strip()
    if len(cleaned) < 8:
        raise ValueError("New password must be at least 8 characters")

    await db.users.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "hashedPassword": hash_password(cleaned),
                "mustChangePassword": False,
                "updatedAt": utc_now(),
            }
        },
    )


async def delete_user(db: AsyncIOMotorDatabase, user_id: str) -> bool:
    user = await get_user_by_id(db, user_id)
    if user is None:
        return False
    await db.passkeys.delete_many({"userId": user["_id"]})
    result = await db.users.delete_one({"_id": user["_id"]})
    return result.deleted_count > 0


async def count_admins(db: AsyncIOMotorDatabase) -> int:
    return await db.users.count_documents({"role": "admin", "active": {"$ne": False}})


async def set_user_active(db: AsyncIOMotorDatabase, user_id: str, *, active: bool) -> dict[str, Any] | None:
    user = await get_user_by_id(db, user_id)
    if user is None:
        return None
    await db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"active": active, "updatedAt": utc_now()}},
    )
    updated = await get_user_by_id(db, user_id)
    if updated is None:
        return None
    count = await db.passkeys.count_documents({"userId": updated["_id"]})
    return serialize_user(updated, passkey_count=count)


async def reset_user_password(
    db: AsyncIOMotorDatabase,
    user: dict[str, Any],
    *,
    new_password: str,
) -> None:
    from services.webauthn_service import delete_all_user_passkeys

    await delete_all_user_passkeys(db, user["_id"])
    await db.users.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "hashedPassword": hash_password(new_password.strip()),
                "mustChangePassword": True,
                "updatedAt": utc_now(),
            }
        },
    )


async def update_user(
    db: AsyncIOMotorDatabase,
    user_id: str,
    *,
    display_name: str | None = None,
    email: str | None = None,
    role: str | None = None,
) -> dict[str, Any] | None:
    user = await get_user_by_id(db, user_id)
    if user is None:
        return None

    updates: dict[str, Any] = {"updatedAt": utc_now()}
    if display_name is not None:
        updates["displayName"] = display_name.strip()
    if email is not None:
        cleaned_email = email.strip().lower()
        existing = await get_user_by_email(db, cleaned_email)
        if existing and existing["_id"] != user["_id"]:
            raise ValueError(f"Email '{cleaned_email}' is already in use")
        updates["email"] = cleaned_email
    if role is not None:
        cleaned_role = role.strip().lower()
        if cleaned_role not in VALID_ROLES:
            raise ValueError(f"Invalid role '{role}'")
        updates["role"] = cleaned_role

    await db.users.update_one({"_id": user["_id"]}, {"$set": updates})
    updated = await get_user_by_id(db, user_id)
    if updated is None:
        return None
    count = await db.passkeys.count_documents({"userId": updated["_id"]})
    return serialize_user(updated, passkey_count=count)
