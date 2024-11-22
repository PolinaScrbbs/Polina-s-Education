from typing import Optional
from pydantic import BaseModel

from .models import Role


class ID(BaseModel):
    id: int


class UserCreate(BaseModel):
    username: str
    password: str
    confirm_password: str
    full_name: str


class BaseUser(ID):
    username: str
    role: str
    full_name: str


class UserResponse(BaseModel):
    message: str
    user: BaseUser


class GetUserFilters(BaseModel):
    role: Optional[Role] = Role.STUDENT
