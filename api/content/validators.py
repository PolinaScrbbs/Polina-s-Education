from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Content


async def content_exists(session: AsyncSession, title: str, file_path: str) -> bool:
    query = select(
        exists().where(
            Content.title == title,
            Content.file_path == file_path,
        )
    )
    result = await session.scalar(query)
    return result
