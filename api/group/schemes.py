from pydantic import BaseModel

from ..user.schemes import ID


class SpecializationCreate(BaseModel):
    code: str
    title: str


class SpecializationInDB(SpecializationCreate, ID):
    pass
