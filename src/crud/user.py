from typing import Optional
from models import User
from tortoise.expressions import Q


async def is_exists(username: Optional[str] = None, email: Optional[str] = None) -> tuple[bool, bool]:
    if (not username and not email):
        return False, False

    query = Q()
    if username:
        query |= Q(username=username)
    if email:
        query |= Q(email=email)

    user = await User.filter(query).first()

    if not user:
        return False, False

    return bool(user.username), bool(user.email)