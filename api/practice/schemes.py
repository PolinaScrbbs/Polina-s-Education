from datetime import datetime
from typing import Optional
from fastapi import Query
from pydantic import BaseModel

from ..user.schemes import ID, BaseUser
from .models import PracticeType


class PracticeCreate(BaseModel):
    title: str
    description: str
    type: PracticeType
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None


class PracticeWitoutCreator(PracticeCreate, ID):
    pass


class PracticeInDB(PracticeWitoutCreator):
    creator: BaseUser


class GetPracticeFilters(BaseModel):
    creator_id: Optional[int]
