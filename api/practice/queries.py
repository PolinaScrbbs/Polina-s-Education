from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Specialization
from .schemes import SpecializationCreate
from .validators import specialization_exists


async def create_specialization(
    session: AsyncSession, specialization_create: SpecializationCreate
) -> Specialization:
    exist = await specialization_exists(
        session, specialization_create.code, specialization_create.title
    )

    if exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Код или специальность с таким названием уже существует",
        )

    new_specialization = Specialization(
        code=specialization_create.code, title=specialization_create.title
    )

    session.add(new_specialization)
    await session.commit()
    await session.refresh(new_specialization)

    return new_specialization


async def get_specializations(session: AsyncSession) -> List[Specialization]:
    result = await session.execute(
        select(Specialization).order_by(Specialization.title)
    )
    specializations = result.scalars().all()

    if not specializations:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="Список специальностей пуст"
        )

    return specializations


async def get_specialization(
    session: AsyncSession, id: Optional[int], code: Optional[str], title: Optional[str]
) -> Specialization:
    if not any([id, code, title]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Введите хотя бы один параметр: id, code или title.",
        )

    query = select(Specialization)
    if id:
        query = query.where(Specialization.id == id)
    elif code:
        query = query.where(Specialization.code == code)
    elif title:
        query = query.where(Specialization.title == title)

    result = await session.execute(query)
    specialization = result.scalar_one_or_none()

    if not specialization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Специальность не найдена."
        )

    return specialization
