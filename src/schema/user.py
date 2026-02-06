from enums import Role
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: str


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr] = None
    password: Optional[str]


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr]
    role: Role

    model_config = ConfigDict(from_attributes=True)