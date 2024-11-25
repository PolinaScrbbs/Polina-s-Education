from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from ..user.schemes import ID, BaseUser
from .models import LessonType, LessonResultStatus


class LessonCreate(BaseModel):
    title: str
    description: str
    type: LessonType = LessonType.PRACTICE


class LessonInDB(LessonCreate, ID):
    pass


class GetLessonFilters(BaseModel):
    title: Optional[str] = None
    type: LessonType = LessonType.PRACTICE


class LessonResultInDB(ID):
    lesson: LessonInDB
    status: LessonResultStatus
    student: BaseUser
    created_at: datetime
    last_updated_at: Optional[datetime]


class GetLessonResultFilters(BaseModel):
    lesson_id: int
    student_id: Optional[int] = None
    status: Optional[LessonResultStatus] = None
