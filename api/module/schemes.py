from datetime import datetime
from typing import Optional
from fastapi import Query
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


class ModuleResultInDB(ID):
    module: ModuleWithoutCreator
    student: BaseUser
    completed_lessons_count: int
    created_at: datetime


class GetModuleResultFilters(BaseModel):
    module_id: Optional[int] = Query(None, description="ID модуля")
    student_id: Optional[int] = Query(None, description="ID студента")
