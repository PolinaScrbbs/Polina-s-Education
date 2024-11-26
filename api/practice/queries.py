from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
import pytz
from sqlalchemy import insert
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Practice, Specialization, PracticePattern, practice_modules
from .schemes import (
    PracticePatternInDB,
    SpecializationCreate,
    PracticePatternCreate,
    GetPracticePatternsFilters,
    PracticeCreate,
    GetPracticeFilters,
)
from . import validators as validator


async def create_specialization(
    session: AsyncSession, specialization_create: SpecializationCreate
) -> Specialization:
    exist = await validator.specialization_exists(
        session, specialization_create.code, specialization_create.title
    )

    if exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Код или специальность с таким названием уже существует",
        )

    new_specialization = Specialization(
        code=specialization_create.code, title=specialization_create.title
    )

    session.add(new_specialization)
    await session.commit()
    await session.refresh(new_specialization)

    return new_specialization


async def get_specializations(session: AsyncSession) -> List[Specialization]:
    result = await session.execute(
        select(Specialization).order_by(Specialization.title)
    )
    specializations = result.scalars().all()

    if not specializations:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return specializations


async def get_specialization(
    session: AsyncSession, id: Optional[int], code: Optional[str], title: Optional[str]
) -> Specialization:
    if not any([id, code, title]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Введите хотя бы один параметр: id, code или title.",
        )

    query = select(Specialization)
    if id:
        query = query.where(Specialization.id == id)
    elif code:
        query = query.where(Specialization.code == code)
    elif title:
        query = query.where(Specialization.title == title)

    result = await session.execute(query)
    specialization = result.scalar_one_or_none()

    if not specialization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Специальность не найдена."
        )

    return specialization


async def create_practice_pattern(
    session: AsyncSession, practice_pattern_create: PracticePatternCreate
) -> PracticePattern:
    exist = await validator.specialization_exists_by_id(
        session, practice_pattern_create.specialization_id
    )

    if not exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Специальность не найдена"
        )

    exist = await validator.practice_pattern_exists(
        session,
        practice_pattern_create.type,
        practice_pattern_create.specialization_id,
        practice_pattern_create.course_number,
    )

    if exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Паттерн уже существует",
        )

    new_practice_pattern = PracticePattern(
        type=practice_pattern_create.type,
        specialization_id=practice_pattern_create.specialization_id,
        course_number=practice_pattern_create.course_number,
    )

    session.add(new_practice_pattern)
    await session.commit()
    await session.refresh(new_practice_pattern)

    return new_practice_pattern


async def get_practice_patterns(
    session: AsyncSession, filters: Optional[GetPracticePatternsFilters]
) -> List[PracticePattern]:
    query = select(PracticePattern)
    if filters:
        if filters.type is not None:
            query = query.where(PracticePattern.type == filters.type)
        if filters.specialization_id is not None:
            query = query.where(
                PracticePattern.specialization_id == filters.specialization_id
            )
        if filters.course_number is not None:
            query = query.where(PracticePattern.course_number == filters.course_number)

    result = await session.execute(query)
    practice_patterns = result.scalars().all()

    if not practice_patterns:
        if not filters:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Паттерн(ы), удовлетворяющий(ие) фильтрам не найден(ы)",
            )

    return practice_patterns


async def get_practice_pattern_by_id(
    session: AsyncSession, practice_pattern_id: int
) -> PracticePatternInDB:
    result = await session.execute(
        select(PracticePattern).where(PracticePattern.id == practice_pattern_id)
    )
    practice_pattern = result.scalar_one_or_none()

    if not practice_pattern:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Паттерн не найден"
        )

    return practice_pattern


async def create_practice(
    session: AsyncSession, practice_create: PracticeCreate, current_user_id: int
) -> Practice:
    exist = await validator.practice_create_validate(
        session,
        practice_create.title,
        practice_create.pattern_id,
        (
            practice_create.start_at
            if practice_create.start_at
            else datetime.now(pytz.timezone("Europe/Moscow")).replace(tzinfo=None)
        ),
    )

    if not exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="В этом учебном году уже запланирована подобная практика",
        )

    new_practice = Practice(
        title=practice_create.title,
        description=practice_create.description,
        pattern_id=practice_create.pattern_id,
        creator_id=current_user_id,
        start_at=practice_create.start_at,
        end_at=practice_create.end_at,
    )

    session.add(new_practice)
    await session.commit()
    await session.refresh(new_practice)
    return new_practice


async def get_practices(
    session: AsyncSession, filters: GetPracticeFilters
) -> List[Practice]:
    print(f"ТУТТ {filters}")
    query = select(Practice)
    if filters:
        if filters.pattern_id:
            query = query.where(Practice.pattern_id == filters.pattern_id)
        if filters.creator_id:
            query = query.where(Practice.creator_id == filters.creator_id)

    result = await session.execute(query.options(selectinload(Practice.creator)))
    practices = result.scalars().all()

    if not practices:
        if not filters:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Практика(и), удовлетворяющая(ие) фильтрам не найдена(ы)",
            )

    return practices


async def get_practice_by_id(session: AsyncSession, practice_id: int) -> Practice:
    result = await session.execute(
        select(Practice)
        .where(Practice.id == practice_id)
        .options(selectinload(Practice.creator))
    )

    practice = result.scalar_one_or_none()

    if not practice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Практика не найдена"
        )

    return practice


async def add_module_to_practice(
    session: AsyncSession,
    current_user_id: int,
    practice_id: int,
    module_id: int,
    number: int,
) -> None:
    exist = await validator.practice_creator_exists(
        session, practice_id, current_user_id
    )
    if not exist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не имеете доступа к чужим практикам",
        )

    await validator.PracticeModulesValidator(
        practice_id, module_id, number, session
    ).validate()

    stmt = insert(practice_modules).values(
        practice_id=practice_id, module_id=module_id, number=number
    )
    await session.execute(stmt)
    await session.commit()
