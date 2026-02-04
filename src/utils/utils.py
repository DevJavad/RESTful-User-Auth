import jwt
from models.user import User
from fastapi import Depends
from passlib.hash import pbkdf2_sha256
from fastapi.responses import JSONResponse
from typing import Literal, Optional, Any
from datetime import datetime, timedelta, UTC
from core.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


bearer_scheme = HTTPBearer()

ALGORITHM = "HS256"
SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_response(
    status: Literal["success", "error"],
    message: str,
    status_code: int = 200,
    *,
    data: Optional[Any] = None,
    error: Optional[Any] = None,
) -> JSONResponse:
    response = {"status": status, "message": message}
    if data:
        response["data"] = data
    if error:
        response["error"] = error

    return JSONResponse(response, status_code)


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pbkdf2_sha256.verify(password, hash)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(
        UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload or "sub" not in payload:
        return create_response("error", "token not valid", 401, error="INVALID_TOKEN")

    user = await User.get_or_none(id=int(payload["sub"]))

    if not user:
        return create_response("error", "user not found", 401, error="USER_EXISTS")

    return user