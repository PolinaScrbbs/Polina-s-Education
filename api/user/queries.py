from typing import List
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..module.models import Module, ModuleResult
from ..lesson.models import Lesson, LessonResult
from .models import User
from .schemes import GetUserFilters, GetModuleLessonResultFilters


async def get_users(session: AsyncSession, filters: GetUserFilters) -> List[User]:
    query = select(User)

    if filters:
        if filters.role:
            query = query.where(User.role == filters.role)

    result = await session.execute(query)
    users = result.scalars().all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователи не найдены"
        )

    return users


async def get_user_by_username(session: AsyncSession, username: str) -> User:

    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    return user


async def get_user_by_id(session: AsyncSession, id: int) -> User:
    result = await session.execute(select(User).where(User.id == id))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    return user


async def get_module_results(
    session: AsyncSession, current_user_id: int
) -> List[ModuleResult]:
    result = await session.execute(
        select(ModuleResult)
        .options(selectinload(ModuleResult.module))
        .where(ModuleResult.student_id == current_user_id)
    )

    module_results = result.scalars().all()

    if not module_results:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return module_results


async def get_module_lessons_results(
    session: AsyncSession, filters: GetModuleLessonResultFilters, current_user_id: int
) -> List[LessonResult]:
    query = (
        select(LessonResult)
        .options(selectinload(LessonResult.lesson), selectinload(LessonResult.contents))
        .join(LessonResult.lesson)
        .join(Lesson.modules)
        .where(
            Lesson.modules.any(Module.id == filters.module_id),
            LessonResult.student_id == current_user_id,
        )
    )

    if filters.lesson_id:
        query = query.where(Lesson.id == filters.lesson_id)

    if filters.lesson_status:
        query = query.where(LessonResult.status == filters.lesson_status)

    results = await session.execute(query)
    lesson_results = results.scalars().all()

    if not lesson_results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Список ваших результатов по урокам модуля пуст или не найдены по соответсвующим фильтрам",
        )

    return lesson_results
