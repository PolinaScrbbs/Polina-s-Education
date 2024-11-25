from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import LessonResult


async def lesson_result_exists(
    session: AsyncSession, lesson_id: int, student_id: int
) -> bool:
    query = select(
        exists().where(
            LessonResult.lesson_id == lesson_id,
            LessonResult.student_id == student_id,
        )
    )
    result = await session.scalar(query)
    return result
