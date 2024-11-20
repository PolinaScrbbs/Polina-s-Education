from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Specialization, PracticePattern


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
