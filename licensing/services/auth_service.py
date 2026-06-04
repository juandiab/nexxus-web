import bcrypt
from datetime import datetime, timedelta, timezone

import jwt

from config import settings

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.jwt_expire_hours)
    payload = {"sub": subject, "exp": expire, "iat": datetime.now(timezone.utc), "typ": "access"}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[ALGORITHM])
        if payload.get("typ") not in (None, "access"):
            return None
        subject = payload.get("sub")
        return subject if isinstance(subject, str) else None
    except jwt.PyJWTError:
        return None
