from typing import Optional
from pydantic import BaseModel

from ..user.schemes import ID
from .models import LessonType


class LessonCreate(BaseModel):
    title: str
    description: str
    type: LessonType = LessonType.PRACTICE


class LessonInDB(LessonCreate, ID):
    pass


class GetLessonFilters(BaseModel):
    title: Optional[str] = None
    type: LessonType = LessonType.PRACTICE
