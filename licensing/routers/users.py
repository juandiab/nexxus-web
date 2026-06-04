from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from dependencies import get_db, require_admin
from models.user import serialize_user
from schemas.auth import MessageResponse
from schemas.user import (
    UserActiveRequest,
    UserCreateRequest,
    UserDetailResponse,
    UserListItem,
    UserUpdateRequest,
)
from services.email_service import (
    generate_temporary_password,
    send_password_reset_email,
    send_welcome_credentials_email,
)
from services.user_service import (
    count_admins,
    create_user,
    delete_user,
    get_user_by_id,
    list_users,
    reset_user_password,
    set_user_active,
    update_user,
)
from services.webauthn_service import delete_passkey, list_user_passkeys

router = APIRouter(prefix="/users", tags=["users"])


def _serialize_passkeys(passkeys: list[dict]) -> list[dict]:
    return [
        {
            "id": str(item["_id"]),
            "label": item.get("label") or "Passkey",
            "createdAt": item.get("createdAt"),
            "lastUsedAt": item.get("lastUsedAt"),
        }
        for item in passkeys
    ]


@router.get("", response_model=list[UserListItem])
async def get_users(
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_admin),
) -> list[UserListItem]:
    return [UserListItem(**row) for row in await list_users(db)]


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_admin),
) -> UserDetailResponse:
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    passkeys = await list_user_passkeys(db, user["_id"])
    row = serialize_user(user, passkey_count=len(passkeys))
    row["passkeys"] = _serialize_passkeys(passkeys)
    return UserDetailResponse(**row)


@router.post("", response_model=UserListItem, status_code=status.HTTP_201_CREATED)
async def post_user(
    payload: UserCreateRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_admin),
) -> UserListItem:
    temporary_password = generate_temporary_password()
    try:
        row = await create_user(
            db,
            username=payload.username,
            display_name=payload.displayName,
            email=payload.email,
            password=temporary_password,
            role=payload.role,
            must_change_password=True,
        )
        await send_welcome_credentials_email(
            to_address=payload.email,
            display_name=payload.displayName,
            username=payload.username.strip().lower(),
            temporary_password=temporary_password,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    return UserListItem(**row)


@router.put("/{user_id}", response_model=UserListItem)
async def put_user(
    user_id: str,
    payload: UserUpdateRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(require_admin),
) -> UserListItem:
    if payload.role != "admin":
        target = await get_user_by_id(db, user_id)
        if target and target.get("role") == "admin" and await count_admins(db) <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot demote the last admin user",
            )
    try:
        updated = await update_user(
            db,
            user_id,
            display_name=payload.displayName,
            email=payload.email,
            role=payload.role,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserListItem(**updated)


@router.patch("/{user_id}/active", response_model=UserListItem)
async def patch_user_active(
    user_id: str,
    payload: UserActiveRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(require_admin),
) -> UserListItem:
    if str(current_user["_id"]) == user_id and not payload.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot deactivate your own account",
        )

    target = await get_user_by_id(db, user_id)
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not payload.active and target.get("role") == "admin" and await count_admins(db) <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate the last admin user",
        )

    updated = await set_user_active(db, user_id, active=payload.active)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserListItem(**updated)


@router.post("/{user_id}/reset-password", response_model=MessageResponse)
async def post_reset_password(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_admin),
) -> MessageResponse:
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    email = (user.get("email") or "").strip()
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no email address on file",
        )

    temporary_password = generate_temporary_password()
    try:
        await reset_user_password(db, user, new_password=temporary_password)
        await send_password_reset_email(
            to_address=email,
            display_name=user.get("displayName") or user["username"],
            username=user["username"],
            temporary_password=temporary_password,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc

    return MessageResponse(message="Password reset email sent")


@router.delete("/{user_id}", response_model=MessageResponse)
async def remove_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(require_admin),
) -> MessageResponse:
    if str(current_user["_id"]) == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot delete your own account")

    target = await get_user_by_id(db, user_id)
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if target.get("role") == "admin" and await count_admins(db) <= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete the last admin user")

    await delete_user(db, user_id)
    return MessageResponse(message="User deleted")


@router.delete("/{user_id}/passkeys/{passkey_id}", response_model=MessageResponse)
async def remove_passkey(
    user_id: str,
    passkey_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_admin),
) -> MessageResponse:
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        oid = ObjectId(passkey_id)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid passkey id") from exc

    passkeys = await list_user_passkeys(db, user["_id"])
    owned = next((item for item in passkeys if item["_id"] == oid), None)
    if owned is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Passkey not found")

    if len(passkeys) <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove the last passkey — register a replacement first",
        )

    await delete_passkey(db, oid)
    return MessageResponse(message="Passkey removed")
