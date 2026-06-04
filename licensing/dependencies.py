from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from db import get_database
from services.auth_service import decode_access_token
from services.user_service import get_user_by_username
from models.user import is_user_active

security = HTTPBearer(auto_error=False)


def get_db():
    return get_database()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = decode_access_token(credentials.credentials)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user_by_username(get_database(), username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not is_user_active(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated.",
        )
    return user


async def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict | None:
    if credentials is None or credentials.scheme.lower() != "bearer":
        return None
    username = decode_access_token(credentials.credentials)
    if username is None:
        return None
    return await get_user_by_username(get_database(), username)


async def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user


async def require_licensing_access(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user.get("role") not in ("admin", "licensing"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Licensing access required")
    return current_user
