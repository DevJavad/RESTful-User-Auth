from enums import Role
from models import User
from .config import settings
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


oauth2 = OAuth2PasswordBearer("login")


async def get_current_user(token: str = Depends(oauth2)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "INVALID_TOKEN"
            )

        user = await User.get(id=user_id)
        if user is None:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "USER_NOT_FOUND"
            )

        return user

    except JWTError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "INVALID_TOKEN"
        )


async def admin_required(user: User = Depends(get_current_user)):
    if user.role not in [Role.ADMIN, Role.OWNER]:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "ADMIN_ACCESS_REQUIRE"
        )
    return user


async def owner_required(user: User = Depends(get_current_user)):
    if user.role != Role.OWNER:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "OWNER_ACCESS_REQUIRE"
        )