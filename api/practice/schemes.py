from pydantic import BaseModel


class ID(BaseModel):
    id: int


class SpecializationCreate(BaseModel):
    code: str
    title: str


class SpecializationInDB(SpecializationCreate, ID):
    pass
