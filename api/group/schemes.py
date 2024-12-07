from pydantic import BaseModel

from ..user.schemes import ID


class SpecializationCreate(BaseModel):
    title: str


class SpecializationInDB(SpecializationCreate, ID):
    pass
