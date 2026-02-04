import schema
from models import User
from fastapi import APIRouter, Depends
from utils import create_response, hash_password, verify_password, create_access_token, get_current_user


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/create")
async def create_user(data: schema.user.User):
    username, password = data.username.lower(), data.password

    if await User.get_or_none(username=username):
        return create_response(
            "error", "username already exists", 409,
            error="EXISTS_USERNAME"
        )

    user = await User.create(
        username=username,
        password=hash_password(password)
    )

    return create_response(
        "success", "Created a new user", 201,
        data={"user_id": user.id}
    )


@router.post("/login")
async def login_user(data: schema.user.User):
    username, password = data.username.lower(), data.password

    user = await User.get_or_none(username=username)

    if not user:
        return create_response("error", "username not exists", 401, error="INVALID_USERNAME")

    if not verify_password(password, user.password):
        return create_response("error", "password not correct", 401, error="INVALID_PASSWORD")

    return create_response(
        "success", "login successful",
        data={
            "access_token": create_access_token({"sub": str(user.id)}),
            "token_type": "bearer"
        }
    )


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return create_response(
        "success",
        "current user info",
        data={"id": current_user.id, "username": current_user.username}
    )


@router.patch("/update")
async def update_user(data: schema.user.User, current_user: User = Depends(get_current_user)):
    update_data = {}
    username, password = data.username.lower(), data.password

    if username:
        update_data["username"] = username
    if password:
        update_data["password"] = hash_password(password)

    if update_data:
        await User.filter(id=current_user.id).update(**update_data)

    return create_response("success", "user updated successfully")


@router.delete("/delete")
async def delete_user(current_user: User = Depends(get_current_user)):
    await User.filter(id=current_user.id).delete()
    return create_response("success", "user deleted successfully")