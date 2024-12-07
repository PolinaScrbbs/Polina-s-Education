from datetime import datetime
from typing import Optional
from fastapi import Query
from pydantic import BaseModel

from ..user.schemes import ID, BaseUser
from .models import PracticeType


class PracticePatternCreate(BaseModel):
    type: PracticeType = PracticeType.EDUCATIONAL_PRACTICE
    specialization_id: int
    course_number: int = 3


class PracticePatternInDB(PracticePatternCreate, ID):
    pass


class GetPracticePatternsFilters(BaseModel):
    type: Optional[PracticeType] = Query(
        PracticeType.EDUCATIONAL_PRACTICE, description="Тип практики"
    )
    specialization_id: Optional[int] = Query(None, description="ID специальности")
    course_number: Optional[int] = Query(None, description="Номер курса")


class PracticeCreate(BaseModel):
    title: str
    description: str
    pattern_id: int
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None


class PracticeWitoutCreator(PracticeCreate, ID):
    pass


class PracticeInDB(PracticeWitoutCreator):
    creator: BaseUser


class GetPracticeFilters(BaseModel):
    pattern_id: Optional[int] = Query(None, description="Патерн Практик")
    creator_id: Optional[int] = Query(None, description="Создатель практики")
