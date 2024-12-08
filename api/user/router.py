from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from .models import User, Role
from .utils import role_check

from ..group.queries import get_group_with_practices
from ..group.schemes import GroupWithPractices
from . import queries as qr
from .schemes import (
    BaseUser,
    GetUserFilters,
    ModuleResult,
    GetModuleLessonResultFilters,
    LessonResult,
)

router = APIRouter(prefix="/user")


@router.get("s/roles", response_model=List[Role])
async def get_roles(
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN],
        "Только администраторы имеют доступ к данному ендпоинту",
    )
    return await Role.values()


@router.get("s", response_model=List[BaseUser])
async def get_users(
    filters: GetUserFilters = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN],
        "Только администраторы имеют доступ к данному ендпоинту",
    )
    users = await qr.get_users(session, filters)
    return users


@router.get("/me", response_model=BaseUser)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get("", response_model=BaseUser)
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN, Role.TEACHER],
        "Студенты не имеют доступа к данному ендпоинту",
    )

    user = await qr.get_user_by_id(session, user_id)
    return user


@router.get("/@{username}", response_model=BaseUser)
async def get_user_by_username(
    username: str,
    session: AsyncSession = Depends(get_session),
):
    user = await qr.get_user_by_username(session, username)
    return user


@router.get("/group/practices", response_model=List[GroupWithPractices])
async def get_group_practices(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.STUDENT],
        "Только студенты имеют доступ к данному ендпоинту",
    )

    practices = await get_group_with_practices(session, current_user.group_id)
    return practices


@router.get("/module/results", response_model=List[ModuleResult])
async def get_modules_results(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.STUDENT],
        "Только студенты имеют доступ к данному ендпоинту",
    )

    module_results = await qr.get_module_results(session, current_user.id)
    return module_results


@router.get("/module/lessons/results", response_model=List[LessonResult])
async def get_module_lessons_results(
    filters: GetModuleLessonResultFilters = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.STUDENT],
        "Только студенты имеют доступ к данному ендпоинту",
    )

    module_lessons_result = await qr.get_module_lessons_results(
        session, filters, current_user.id
    )
    return module_lessons_result
