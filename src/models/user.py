from tortoise.models import Model
from tortoise.fields import IntField, CharField


class User(Model):
    id = IntField(pk=True)
    username = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)

    class Meta:
        table = "users"

    def __str__(self):
        return self.username