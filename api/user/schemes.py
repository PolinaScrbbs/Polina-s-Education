from datetime import datetime
from typing import List, Optional
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


class Module(ID):
    title: str
    description: str
    is_mandatory: bool


class ModuleResult(ID):
    module: Module
    completed_lessons_count: int
    created_at: datetime


class UserWithModuleResult(BaseUser):
    module_results: List[ModuleResult]
