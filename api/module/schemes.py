from pydantic import BaseModel

from ..user.schemes import ID, BaseUser


class ModuleCreate(BaseModel):
    title: str
    description: str
    is_mandatory: bool = True


class ModuleWithoutCreator(ModuleCreate, ID):
    pass


class ModuleInDB(ModuleWithoutCreator):
    creator: BaseUser
