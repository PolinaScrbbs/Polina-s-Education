from typing import List
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Module, ModuleResult
from .schemes import (
    GetModuleResultFilters,
    ModuleCreate,
)
from . import validators as validator


async def create_module(
    session: AsyncSession, module_create: ModuleCreate, current_user_id: int
) -> Module:
    new_module = Module(
        title=module_create.title,
        description=module_create.description,
        creator_id=current_user_id,
        is_mandatory=module_create.is_mandatory,
    )

    session.add(new_module)
    await session.commit()
    await session.refresh(new_module)
    return new_module


async def get_modules(session: AsyncSession) -> List[Module]:
    result = await session.execute(
        select(Module).options(selectinload(Module.creator)).order_by(Module.title)
    )
    modules = result.scalars().all()

    if not modules:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return modules


async def get_module_by_id(session: AsyncSession, module_id: int) -> Module:
    result = await session.execute(
        select(Module)
        .options(selectinload(Module.creator))
        .where(Module.id == module_id)
    )

    module = result.scalar_one_or_none()

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Модуль не найден"
        )

    return module


async def create_module_result(
    session: AsyncSession, module_id: int, current_user_id: int
) -> None:
    exist = await validator.module_result_exists(session, module_id, current_user_id)

    if exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Вы уже начинали этот модуль"
        )

    new_module_result = ModuleResult(module_id=module_id, student_id=current_user_id)

    session.add(new_module_result)
    await session.commit()


async def get_results(
    session: AsyncSession, filters: GetModuleResultFilters
) -> List[ModuleResult]:
    query = select(ModuleResult).options(
        selectinload(ModuleResult.module), selectinload(ModuleResult.student)
    )

    if filters:
        if filters.module_id:
            query = query.where(ModuleResult.module_id == filters.module_id)
        if filters.student_id:
            query = query.where(ModuleResult.student_id == filters.student_id)

    result = await session.execute(query)
    results = result.scalars().all()

    if not results:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return results
