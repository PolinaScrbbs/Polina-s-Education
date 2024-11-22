from typing import List, Optional
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from .models import User, Role
from .utils import role_check

from . import queries as qr
from .schemes import BaseUser, GetUserFilters

router = APIRouter(prefix="/user")


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
