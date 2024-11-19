from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Specialization


async def specialization_exists(
    session: AsyncSession, code: str = None, title: str = None
) -> bool:
    query = select(
        exists().where((Specialization.code == code) | (Specialization.title == title))
    )
    result = await session.scalar(query)
    return result
