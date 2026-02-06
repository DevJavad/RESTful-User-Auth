from enums import Role
from tortoise.models import Model
from tortoise.fields import (
    IntField,
    CharField,
    DatetimeField,
    CharEnumField
)


class User(Model):
    id = IntField(pk=True)
    username = CharField(max_length=50, unique=True)
    email = CharField(max_length=100, unique=True)
    password = CharField(max_length=100)
    role = CharEnumField(Role, default=Role.USER)
    create_at = DatetimeField(auto_now_add=True)
    update_at = DatetimeField(auto_now=True)

    class Meta:
        table = "users"

    def __str__(self):
        return f"User(username={self.username}, email={self.email}, role={self.role})"