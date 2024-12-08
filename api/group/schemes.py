from typing import List, Optional
from pydantic import BaseModel

from ..user.schemes import ID, BaseUser


class SpecializationCreate(BaseModel):
    code: str
    title: str


class SpecializationInDB(SpecializationCreate, ID):
    pass


class GroupCreate(BaseModel):
    specialization_id: int
    course: int
    director_id: Optional[int] = None
    is_commeration: bool = False


class GroupWithOutStudents(ID):
    number: str
    specialization: str
    course: int
    director: BaseUser


class GroupWithStudents(GroupWithOutStudents):
    students: List[BaseUser]


class GroupWithOutSpecialization(ID):
    number: str
    course: int
    director: BaseUser


class SpecializationWithGroups(BaseModel):
    title: str
    code: str
    groups: List[GroupWithOutSpecialization]
