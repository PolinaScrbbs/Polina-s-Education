from sqlalchemy.ext.asyncio import AsyncSession

from .models import Lesson
from .schemes import LessonCreate


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
