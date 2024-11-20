from typing import Optional
from fastapi import Query
from pydantic import BaseModel
from .models import PracticeType


class ID(BaseModel):
    id: int


class SpecializationCreate(BaseModel):
    code: str
    title: str


class SpecializationInDB(SpecializationCreate, ID):
    pass


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
