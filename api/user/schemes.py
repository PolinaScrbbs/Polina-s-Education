from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from ..lesson.models import LessonType, LessonResultStatus
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


class GetModuleLessonResultFilters(BaseModel):
    module_id: int
    lesson_id: Optional[int] = None
    lesson_status: Optional[LessonResultStatus] = None


class Lesson(ID):
    title: str
    description: str
    type: LessonType


class Content(ID):
    title: str
    description: str
    file_path: str
    created_at: datetime
    last_updated_at: Optional[datetime] 


class LessonResult(ID):
    lesson: Lesson
    status: LessonResultStatus
    contents: List[Content]
    created_at: datetime
    last_updated_at: Optional[datetime]
