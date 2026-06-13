import bcrypt
from datetime import datetime, timedelta, timezone

import jwt

from config import settings

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(subject: str, *, role: str = "user") -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.jwt_expire_hours)
    payload = {
        "sub": subject,
        "role": role.strip().lower(),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "typ": "access",
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str | None:
    claims = decode_token_claims(token)
    if claims is None:
        return None
    subject = claims.get("sub")
    return subject if isinstance(subject, str) else None


def decode_token_claims(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[ALGORITHM])
        if payload.get("typ") not in (None, "access"):
            return None
        return payload
    except jwt.PyJWTError:
        return None
