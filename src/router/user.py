from enums import Role
from models import User
from crud.user import is_exists
from utils.response import success
from schema.user import UserCreate, UserUpdate, UserOut
from fastapi import APIRouter, HTTPException, status, Depends
from core.security import hash_password, verify_password, create_access_token
from core.dependencies import get_current_user, admin_required, owner_required


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/register", response_model=UserOut)
async def register_user(data: UserCreate):
    username, email, password = data.username.lower(), data.email.lower(), data.password
    _username, _email = await is_exists(username, email)

    if (_username and _email):
        raise HTTPException(status.HTTP_409_CONFLICT, "EXISTS_VALUES")
    elif _username:
        raise HTTPException(status.HTTP_409_CONFLICT, "EXISTS_USERNAME")
    elif _email:
        raise HTTPException(status.HTTP_409_CONFLICT, "EXISTS_EMAIL")

    _hash = hash_password(password)
    user = await User.create(username=username, email=email, password=_hash)

    return success("REGISTERE_SUCCESS", UserOut.model_validate(user).model_dump(), 201)


@router.post("/login")
async def login_user(data: UserCreate):
    username, password = data.username.lower(), data.password

    user = await User.get_or_none(username=username)

    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "INVALID_USERNAME")

    if not verify_password(password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "INVALID_PASSWORD")

    token = create_access_token({"sub": str(user.id)})

    return success(
        "LOGIN_SUCCESS",
        {
            "access_token": token,
            "token_type": "bearer",
            "user": UserOut.model_validate(user).model_dump()
        }
    )


@router.get("/me", response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return success("USER_DATA", UserOut.model_validate(user).model_dump())


@router.put("/update", response_model=UserOut)
async def update_user(data: UserUpdate, user: User = Depends(get_current_user)):
    username, email, password = data.username, data.email, data.password
    username = username.lower() if username else None
    email = email.lower() if email else None

    _username, _email = await is_exists(username, email)

    if _username and username != user.username:
        raise HTTPException(status.HTTP_409_CONFLICT, "EXISTS_USERNAME")

    if _email and email != user.email:
        raise HTTPException(status.HTTP_409_CONFLICT, "EXISTS_EMAIL")

    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.password = hash_password(password)

    await user.save()

    return success("UPDATE_USER", UserOut.model_validate(user).model_dump())


@router.delete("/{user_id}")
async def delete_user(user_id: int, admin: User = Depends(admin_required)):
    user = await User.get_or_none(id=user_id)

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "USER_NOT_FOUND")

    await user.delete()

    return success("DELETED_USER")


@router.get("/list")
async def users(admin: User = Depends(admin_required)):
    users = await User.all()

    return success("USERS", [UserOut.model_validate(user).model_dump() for user in users])


@router.post("/{user_id}/promote")
async def promote_user(user_id: int, owner: User = Depends(owner_required)):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "USER_NOT_FOUND")

    if user.role == Role.ADMIN:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "ALREADY_ADMIN")

    user.role = Role.ADMIN
    await user.save()

    return success("PROMOTED_USER")


@router.post("/{user_id}/demtoe")
async def demote_user(user_id: int, owner: User = Depends(owner_required)):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "USER_NOT_FOUND")

    if user.role == Role.ADMIN:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "NOT_ADMIN")

    return success("DEMOTED_USER")