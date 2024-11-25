from typing import List
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Lesson, LessonResult
from .schemes import LessonCreate, GetLessonFilters, GetLessonResultFilters
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
    if filters.with_contents is True:
        query = query.options(selectinload(Lesson.contents))

    result = await session.execute(query)
    lessons = result.scalars().all()

    if not lessons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Список уроков пуст или не найдены уроки, удовлетворяющие фильтрам",
        )

    return lessons


async def get_lesson_by_id(
    session: AsyncSession, lessons_id: int, with_contents: bool
) -> Lesson:
    query = select(Lesson).where(Lesson.id == lessons_id)

    if with_contents is True:
        query = query.options(selectinload(Lesson.contents))

    result = await session.execute(query)
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


async def get_lesson_results(
    session: AsyncSession, filters: GetLessonResultFilters
) -> List[LessonResult]:
    query = (
        select(LessonResult)
        .options(
            selectinload(LessonResult.lesson),
            selectinload(LessonResult.student),
        )
        .where(LessonResult.lesson_id == filters.lesson_id)
    )

    if filters.student_id:
        query = query.where(LessonResult.student_id == filters.student_id)
    if filters.status:
        query = query.where(LessonResult.status == filters.status)

    result = await session.execute(query)
    lesson_results = result.scalars().all()

    if not lesson_results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Список результатов урока пуст или не найдены результаты урока, удовлетворяющие фильтрам",
        )

    return lesson_results


async def get_lesson_result_by_id(
    session: AsyncSession, lesson_result_id: int
) -> LessonResult:
    result = await session.execute(
        select(LessonResult)
        .options(
            selectinload(LessonResult.lesson),
            selectinload(LessonResult.student),
        )
        .where(LessonResult.id == lesson_result_id)
    )

    lesson_result = result.scalar_one_or_none()

    if not lesson_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Результат урока не найден",
        )

    return lesson_result
