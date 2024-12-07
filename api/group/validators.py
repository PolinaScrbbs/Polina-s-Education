from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from ..group.models import Specialization


async def specialization_exists_by_title(
    session: AsyncSession, title: str = None
) -> bool:
    query = select(exists().where(Specialization.title == title))
    result = await session.scalar(query)
    return result


async def specialization_exists_by_id(
    session: AsyncSession, specialization_id: int
) -> bool:
    query = select(exists().where(Specialization.id == specialization_id))
    result = await session.scalar(query)
    return result
