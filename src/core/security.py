import jwt
from typing import Optional
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta, UTC
from core.config import settings


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pbkdf2_sha256.verify(password, hash)


def create_access_token(data: dict, expire: Optional[timedelta] = None):
    to_encode = data.copy()
    _expire = datetime.now(UTC) + (
        expire or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": _expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)