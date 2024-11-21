from pydantic import BaseModel

from ..user.schemes import ID


class ModuleCreate(BaseModel):
    title: str
    description: str
    is_mandatory: bool = True


class ModuleWithoutCreator(ModuleCreate, ID):
    pass
