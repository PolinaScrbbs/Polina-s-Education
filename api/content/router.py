from typing import List
from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User, Role
from ..user.utils import role_check

from . import queries as qr
from .schemes import (
    ContentCreate,
    ContentWithoutCreator,
    ContentInDB,
    GetContentFilters,
)

router = APIRouter(prefix="/content")


@router.post(
    "", response_model=ContentWithoutCreator, status_code=status.HTTP_201_CREATED
)
async def create_content(
    content_create: ContentCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN],
        "Только администратор имеет доступ к данному эндпоинту",
    )
    new_content = await qr.create_content(session, content_create, current_user.id)
    return new_content


@router.get("s", response_model=List[ContentInDB])
async def get_contents(
    filters: GetContentFilters = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN, Role.TEACHER],
        "Этот ендпоинт не доступен студентам",
    )

    contents = await qr.get_contents(session, filters)
    return contents


@router.get("", response_model=ContentInDB)
async def get_content(
    content_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN, Role.TEACHER],
        "Этот ендпоинт не доступен студентам",
    )
    content = await qr.get_content_by_id(session, content_id)
    return content
