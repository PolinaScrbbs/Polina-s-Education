from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Specialization, PracticePattern, Practice


async def specialization_exists(
    session: AsyncSession, code: str = None, title: str = None
) -> bool:
    query = select(
        exists().where((Specialization.code == code) | (Specialization.title == title))
    )
    result = await session.scalar(query)
    return result


async def specialization_exists_by_id(
    session: AsyncSession, specialization_id: int
) -> bool:
    query = select(exists().where(Specialization.id == specialization_id))
    result = await session.scalar(query)
    return result


async def practice_pattern_exists(
    session: AsyncSession, type: str, specialization_id: int, course_number: int
) -> bool:
    query = select(
        exists().where(
            PracticePattern.type == type,
            PracticePattern.specialization_id == specialization_id,
            PracticePattern.course_number == course_number,
        )
    )
    result = await session.scalar(query)
    return result


async def practice_create_validate(
    session: AsyncSession, title: str, pattern_id: int, start_at: Optional[datetime]
) -> bool:
    query = (
        select(Practice)
        .where(
            Practice.title == title,
            Practice.pattern_id == pattern_id,
        )
        .order_by(Practice.start_at.desc())
        .limit(1)
    )

    result = await session.execute(query)
    practice = result.scalar_one_or_none()

    if practice and start_at:
        time_difference = start_at - practice.start_at
        if time_difference < timedelta(days=335):
            return False

    return True
