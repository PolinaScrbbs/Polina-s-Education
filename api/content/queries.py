from typing import List
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Content
from .schemes import ContentCreate, GetContentFilters
from . import validators as validator


async def create_content(
    session: AsyncSession, content_create: ContentCreate, current_user_id: int
) -> Content:
    exist = await validator.content_exists(
        session, content_create.title, content_create.file_path
    )
    if exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Контент с таким названием и содержанием уже существует",
        )

    new_content = Content(
        title=content_create.title,
        description=content_create.description,
        file_path=content_create.file_path,
        creator_id=current_user_id,
    )

    session.add(new_content)
    await session.commit()
    await session.refresh(new_content)
    return new_content


async def get_contents(
    session: AsyncSession, filters: GetContentFilters
) -> List[Content]:
    query = select(Content).options(selectinload(Content.creator))

    if filters.title:
        query = query.where(Content.title == filters.title)
    if filters.creator_id:
        query = query.where(Content.creator_id == filters.creator_id)

    result = await session.execute(query)
    contents = result.scalars().all()

    if not contents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Список контента пуст или не найден контент, удовлетворяющий фильтрам",
        )

    return contents


async def get_content_by_id(session: AsyncSession, content_id: int) -> Content:
    result = await session.execute(
        select(Content)
        .options(selectinload(Content.creator))
        .where(Content.id == content_id)
    )

    content = result.scalar_one_or_none()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Контент не найден"
        )

    return content
