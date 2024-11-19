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
            status.HTTP_409_CONFLICT,
            "Код или специальность с таким названием уже существует",
        )

    new_specialization = Specialization(
        code=specialization_create.code, title=specialization_create.title
    )

    session.add(new_specialization)
    await session.commit()
    await session.refresh(new_specialization)

    return new_specialization
