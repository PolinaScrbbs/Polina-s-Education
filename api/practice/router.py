from typing import List
from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User, Role
from ..user.utils import role_check

from . import queries as qr
from .schemes import (
    PracticeCreate,
    PracticeWitoutCreator,
    PracticeInDB,
    GetPracticeFilters,
)

router = APIRouter(prefix="/practice")


@router.post(
    "",
    response_model=PracticeWitoutCreator,
    status_code=status.HTTP_201_CREATED,
)
async def create_practice(
    practice_create: PracticeCreate = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN],
        "Только администратор имеет доступ к данному эндпоинту",
    )
    new_practice = await qr.create_practice(session, practice_create, current_user.id)
    return new_practice


@router.get("s", response_model=List[PracticeInDB])
async def get_practices(
    filters: GetPracticeFilters = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    practices = await qr.get_practices(session, filters)
    return practices


@router.get("", response_model=PracticeInDB)
async def get_practice_by_id(
    practice_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    practice = await qr.get_practice_by_id(session, practice_id)
    return practice


@router.delete("/{practice_id}", status_code=status.HTTP_200_OK)
async def delete_practice(
    practice_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN],
        "Только администратор имеет доступ к данному эндпоинту",
    )
    await qr.delete_practice(session, practice_id)
    return {"detail": "Практика удалена"}


@router.post("/group/add", status_code=status.HTTP_201_CREATED)
async def add_practice_to_group(
    group_id: int,
    practice_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN],
        "Только администратор имеет доступ к данному эндпоинту",
    )

    await qr.add_practice_to_group(session, group_id, practice_id)
    return {"detail": "Практика добавлена к группе"}


@router.post("/module/add", status_code=status.HTTP_201_CREATED)
async def add_module_to_practice(
    practice_id: int,
    module_id: int,
    number: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN],
        "Только администратор имеет доступ к данному эндпоинту",
    )

    await qr.add_module_to_practice(
        session, current_user.id, practice_id, module_id, number
    )
    return {"detail": "Модуль добавлен в практику"}


@router.delete("/module/remove", status_code=status.HTTP_200_OK)
async def remove_module_from_practice(
    practice_id: int,
    module_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN],
        "Только администратор имеет доступ к данному эндпоинту",
    )

    await qr.remove_module_from_practice(session, practice_id, module_id)
    return {"detail": "Модуль удален из практики"}
