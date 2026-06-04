from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from dependencies import get_db, get_optional_current_user
from models.user import is_user_active, serialize_user
from schemas.auth import LoginResponse, UserResponse
from schemas.webauthn import (
    WebAuthnLoginBeginRequest,
    WebAuthnLoginFinishRequest,
    WebAuthnRegisterBeginRequest,
    WebAuthnRegisterFinishRequest,
    WebAuthnStatusResponse,
    WebAuthnUsernameRequest,
)
from services.auth_service import create_access_token
from services.user_service import get_user_by_username
from services.webauthn_service import (
    begin_authentication,
    begin_registration,
    count_user_passkeys,
    finish_authentication,
    finish_registration,
)

router = APIRouter(prefix="/auth/webauthn", tags=["webauthn"])


async def _build_login_response(db: AsyncIOMotorDatabase, user: dict[str, Any]) -> LoginResponse:
    count = await count_user_passkeys(db, user["_id"])
    return LoginResponse(
        accessToken=create_access_token(user["username"]),
        user=UserResponse(**serialize_user(user, passkey_count=count)),
    )


async def _resolve_user(db: AsyncIOMotorDatabase, username: str) -> dict:
    user = await get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not is_user_active(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated.",
        )
    return user


def _can_register_passkey(user: dict[str, Any], current_user: dict | None) -> bool:
    if current_user is None:
        return False
    return current_user["_id"] == user["_id"] or current_user.get("role") == "admin"


@router.post("/status", response_model=WebAuthnStatusResponse)
async def passkey_status(
    payload: WebAuthnUsernameRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict | None = Depends(get_optional_current_user),
) -> WebAuthnStatusResponse:
    user = await get_user_by_username(db, payload.username)
    if user is None:
        return WebAuthnStatusResponse(
            username=payload.username.strip().lower(),
            exists=False,
            hasPasskey=False,
            passkeyRequired=False,
            canRegister=False,
        )

    passkey_count = await count_user_passkeys(db, user["_id"])
    has_passkey = passkey_count > 0
    active = is_user_active(user)
    return WebAuthnStatusResponse(
        username=user["username"],
        exists=True,
        hasPasskey=has_passkey,
        passkeyRequired=has_passkey and active,
        canRegister=active and _can_register_passkey(user, current_user),
    )


@router.post("/register/begin")
async def register_begin(
    payload: WebAuthnRegisterBeginRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict | None = Depends(get_optional_current_user),
) -> dict[str, Any]:
    user = await _resolve_user(db, payload.username)
    if not _can_register_passkey(user, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Passkey registration is not allowed for this user",
        )
    if user.get("mustChangePassword"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Change your password before registering a passkey",
        )
    if not (user.get("email") or "").strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required before registering a passkey",
        )
    try:
        return await begin_registration(db, user)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/register/finish")
async def register_finish(
    payload: WebAuthnRegisterFinishRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict | None = Depends(get_optional_current_user),
) -> dict[str, Any]:
    user = await _resolve_user(db, payload.username)
    if not _can_register_passkey(user, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Passkey registration is not allowed for this user",
        )
    if user.get("mustChangePassword"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Change your password before registering a passkey",
        )
    try:
        await finish_registration(db, user, payload.credential, label=payload.label)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return {"success": True, "message": "Passkey registered"}


@router.post("/login/begin")
async def login_begin(
    payload: WebAuthnLoginBeginRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> dict[str, Any]:
    user = await _resolve_user(db, payload.username)
    try:
        return await begin_authentication(
            db,
            user,
            prefer_cross_device=payload.preferCrossDevice,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login/finish", response_model=LoginResponse)
async def login_finish(
    payload: WebAuthnLoginFinishRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> LoginResponse:
    user = await _resolve_user(db, payload.username)
    try:
        await finish_authentication(db, user, payload.credential)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    return await _build_login_response(db, user)
