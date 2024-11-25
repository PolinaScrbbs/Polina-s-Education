from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from ..user.schemes import ID, BaseUser
from ..content.schemes import ContentWithoutCreator
from .models import LessonType, LessonResultStatus


class LessonCreate(BaseModel):
    title: str
    description: str
    type: LessonType = LessonType.PRACTICE


class LessonInDB(LessonCreate, ID):
    pass


class LessonWithContent(LessonInDB):
    contents: List[ContentWithoutCreator]


class GetLessonFilters(BaseModel):
    title: Optional[str] = None
    type: LessonType = LessonType.PRACTICE
    with_contents: bool = False


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
