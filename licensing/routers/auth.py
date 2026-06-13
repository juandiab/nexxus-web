from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from dependencies import get_current_user, get_db
from models.user import is_user_active, serialize_user
from schemas.auth import ChangePasswordRequest, LoginRequest, LoginResponse, MessageResponse, UserResponse
from services.auth_service import create_access_token, verify_password
from services.user_service import change_password, get_user_by_username
from services.webauthn_service import count_user_passkeys

router = APIRouter(prefix="/auth", tags=["auth"])


async def _user_response(db: AsyncIOMotorDatabase, user: dict[str, Any]) -> UserResponse:
    count = await count_user_passkeys(db, user["_id"])
    return UserResponse(**serialize_user(user, passkey_count=count))


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)) -> LoginResponse:
    user = await get_user_by_username(db, payload.username)
    hashed = user.get("hashedPassword") if user else None
    if user is None or not hashed or not verify_password(payload.password, hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not is_user_active(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated.",
        )

    passkey_count = await count_user_passkeys(db, user["_id"])
    if passkey_count > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account uses passkey sign-in only.",
        )

    return LoginResponse(
        accessToken=create_access_token(user["username"], role=user.get("role", "user")),
        user=await _user_response(db, user),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> UserResponse:
    return await _user_response(db, current_user)


@router.post("/change-password", response_model=MessageResponse)
async def post_change_password(
    payload: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> MessageResponse:
    try:
        await change_password(
            db,
            current_user,
            current_password=payload.currentPassword,
            new_password=payload.newPassword,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return MessageResponse(message="Password updated")


@router.post("/logout", response_model=MessageResponse)
async def logout(_: dict = Depends(get_current_user)) -> MessageResponse:
    return MessageResponse(message="Logged out successfully")
