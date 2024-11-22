from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from ..user.schemes import ID, BaseUser


class ContentCreate(BaseModel):
    title: str
    description: str
    file_path: str


class ContentWithoutCreator(ContentCreate, ID):
    created_at: datetime
    last_updated_at: Optional[datetime]


class ContentInDB(ContentWithoutCreator):
    creator: BaseUser
