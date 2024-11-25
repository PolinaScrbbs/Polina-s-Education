from typing import List
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Lesson, LessonResult
from .schemes import LessonCreate, GetLessonFilters
from . import validators as validator


async def create_lesson(session: AsyncSession, lesson_create: LessonCreate) -> Lesson:

    new_lesson = Lesson(
        title=lesson_create.title,
        description=lesson_create.description,
        type=lesson_create.type,
    )

    session.add(new_lesson)
    await session.commit()
    await session.refresh(new_lesson)
    return new_lesson


async def get_lessons(session: AsyncSession, filters: GetLessonFilters) -> List[Lesson]:
    query = select(Lesson)

    if filters.title:
        query = query.where(Lesson.title == filters.title)
    if filters.type:
        query = query.where(Lesson.type == filters.type)

    result = await session.execute(query)
    lessons = result.scalars().all()

    if not lessons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Список уроков пуст или не найдены уроки, удовлетворяющие фильтрам",
        )

    return lessons


async def get_lesson_by_id(session: AsyncSession, lessons_id: int) -> Lesson:
    result = await session.execute(select(Lesson).where(Lesson.id == lessons_id))
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Урок не найден",
        )

    return lesson


async def create_lesson_result(
    session: AsyncSession, lesson_id: int, student_id: int
) -> None:
    exist = await validator.lesson_result_exists(session, lesson_id, student_id)
    if exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Вы уже начинали этот урок"
        )

    new_lesson_result = LessonResult(lesson_id=lesson_id, student_id=student_id)

    session.add(new_lesson_result)
    await session.commit()
