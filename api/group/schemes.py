from typing import List, Optional, Union
from pydantic import BaseModel

from ..user.schemes import ID, BaseUser
from ..practice.schemes import PracticeInDB


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
    specialization: Union[str, SpecializationInDB]
    course: int
    director: BaseUser


class GroupWithStudents(GroupWithOutStudents):
    students: List[BaseUser]


class GroupWithPractices(GroupWithOutStudents):
    practices: List[PracticeInDB]


class GroupWithOutSpecialization(ID):
    number: str
    course: int
    director: BaseUser


class SpecializationWithGroups(BaseModel):
    title: str
    code: str
    groups: List[GroupWithOutSpecialization]
