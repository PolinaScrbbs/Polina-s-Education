from typing import List
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Content
from .schemes import ContentCreate
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
