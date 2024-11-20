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
