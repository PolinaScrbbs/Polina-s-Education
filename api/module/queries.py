from typing import List
from fastapi import HTTPException, status
from sqlalchemy import insert
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from api.user.models import Role

from .models import Module, ModuleResult, module_lessons
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


async def get_module_results(
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


async def get_module_result_by_id(
    session: AsyncSession,
    module_result_id: int,
    current_user_id: int,
    current_user_role: Role,
) -> ModuleResult:
    if current_user_role == Role.STUDENT:
        exist = await validator.student_module_result_exists(
            session, module_result_id, current_user_id
        )
        if not exist:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Студент имеет доступ только к своим результатам",
            )

    result = await session.execute(
        select(ModuleResult)
        .options(selectinload(ModuleResult.module), selectinload(ModuleResult.student))
        .where(ModuleResult.id == module_result_id)
    )
    module_result = result.scalar_one_or_none()

    if not module_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Результат модуля не найден"
        )

    return module_result


async def add_lesson_to_module(
    session: AsyncSession, current_user_id, module_id: int, lesson_id: int, number: int
) -> None:
    exist = await validator.module_creator_exists(session, module_id, current_user_id)
    if not exist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не имеете доступа к чужим модулям",
        )

    await validator.ModuleLessonsValidator(
        module_id, lesson_id, number, session
    ).validate()

    stmt = insert(module_lessons).values(
        module_id=module_id, lesson_id=lesson_id, number=number
    )
    await session.execute(stmt)
    await session.commit()
