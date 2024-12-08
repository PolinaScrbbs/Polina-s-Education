from datetime import datetime
from typing import List
from fastapi import HTTPException, status
import pytz
from sqlalchemy import insert, delete
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Practice, group_practice, practice_modules
from .schemes import (
    PracticeCreate,
    GetPracticeFilters,
)
from . import validators as validator


async def create_practice(
    session: AsyncSession, practice_create: PracticeCreate, current_user_id: int
) -> Practice:
    exist = await validator.practice_create_validate(
        session,
        practice_create.title,
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
        type=practice_create.type,
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


async def delete_practice(session: AsyncSession, practice_id: int):
    practice = await session.get(Practice, practice_id)
    if not practice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Практика не найдена",
        )
    await session.delete(practice)
    await session.commit()


async def add_practice_to_group(
    session: AsyncSession,
    group_id: int,
    practice_id: int,
) -> None:

    await validator.GroupPracticeValidator(group_id, practice_id, session).validate()

    stmt = insert(group_practice).values(group_id=group_id, practice_id=practice_id)
    await session.execute(stmt)
    await session.commit()


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


async def remove_module_from_practice(
    session: AsyncSession, practice_id: int, module_id: int
):
    query = select(practice_modules).where(
        (practice_modules.c.practice_id == practice_id)
        & (practice_modules.c.module_id == module_id)
    )
    result = await session.execute(query)
    practice_module = result.scalar_one_or_none()

    if not practice_module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Модуль в указанной практике не найден",
        )

    delete_query = delete(practice_modules).where(
        (practice_modules.c.practice_id == practice_id)
        & (practice_modules.c.module_id == module_id)
    )
    await session.execute(delete_query)
    await session.commit()
