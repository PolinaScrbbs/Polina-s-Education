from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User, Role
from ..user.utils import role_check

from . import queries as qr
from .schemes import (
    ModuleCreate,
    ModuleWithoutCreator,
    ModuleInDB,
    ModuleResultInDB,
    GetModuleResultFilters,
)

router = APIRouter(prefix="/module")


@router.post(
    "", response_model=ModuleWithoutCreator, status_code=status.HTTP_201_CREATED
)
async def create_module(
    module_create: ModuleCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN],
        "Только администратор имеет доступ к данному эндпоинту",
    )
    new_module = await qr.create_module(session, module_create, current_user.id)
    return new_module


@router.get("s", response_model=List[ModuleInDB])
async def get_modules(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    modules = await qr.get_modules(session)
    return modules


@router.get("", response_model=ModuleInDB)
async def get_module_by_id(
    module_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    module = await qr.get_module_by_id(session, module_id)
    return module


@router.post("/result", status_code=status.HTTP_201_CREATED)
async def create_module_result(
    module_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user, [Role.STUDENT], "Только студент имеет доступ к данному эндпоинту"
    )
    await qr.create_module_result(session, module_id, current_user.id)
    return f"Вы, {current_user.username}, начали прохождение модуля"


@router.get("/results", response_model=List[ModuleResultInDB])
async def get_module_results(
    filters: GetModuleResultFilters = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == Role.STUDENT:
        if filters.student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Студенты не имеют доступка к чужим результатам",
            )
        filters.student_id = current_user.id
    results = await qr.get_module_results(session, filters)
    return results


@router.get("/result", response_model=ModuleResultInDB)
async def get_module_result_by_id(
    module_result_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    module_result = await qr.get_module_result_by_id(
        session, module_result_id, current_user.id, current_user.role
    )
    return module_result
