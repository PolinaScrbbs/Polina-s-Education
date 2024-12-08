from typing import List, Optional
from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User, Role
from ..user.utils import role_check

from . import queries as qr
from .schemes import (
    SpecializationCreate,
    SpecializationInDB,
    GroupCreate,
    GroupWithOutStudents,
    SpecializationWithGroups,
)

router = APIRouter(prefix="/group")


@router.post(
    "s/specialization",
    response_model=SpecializationInDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_specialization(
    specialization_create: SpecializationCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN],
        "Только администратор имеет доступ к данному эндпоинту",
    )
    new_specialization = await qr.create_specialization(session, specialization_create)
    return new_specialization


@router.get("s/specializations", response_model=List[SpecializationInDB])
async def get_specializations(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    specializations = await qr.get_specializations(session)
    return specializations


@router.get("s/specialization", response_model=SpecializationInDB)
async def get_specialization(
    id: Optional[int] = None,
    title: Optional[str] = None,
    code: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    specialization = await qr.get_specialization(session, id, code, title)
    return specialization


@router.delete("s/specialization/{specialization_id}", status_code=status.HTTP_200_OK)
async def delete_specialization(
    specialization_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN],
        "Только администратор имеет доступ к данному эндпоинту",
    )
    await qr.delete_specialization(session, specialization_id)
    return {"detail": "Специальность удалена"}


@router.post(
    "", response_model=GroupWithOutStudents, status_code=status.HTTP_201_CREATED
)
async def create_group(
    group_create: GroupCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN],
        "Только администратор имеет доступ к данному эндпоинту",
    )

    new_group = await qr.create_group(session, group_create, current_user.id)
    return new_group


@router.get("s/", response_model=List[SpecializationWithGroups])
async def get_groups(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    groups = await qr.get_groups(session)
    return groups
