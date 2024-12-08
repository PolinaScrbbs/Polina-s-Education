from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..user.queries import get_user_by_id
from ..practice.models import Practice
from .models import Group, Specialization
from .schemes import (
    BaseUser,
    GroupWithOutSpecialization,
    SpecializationCreate,
    GroupCreate,
    GroupWithOutStudents,
    SpecializationWithGroups,
)
from . import validators as validator


async def create_specialization(
    session: AsyncSession, specialization_create: SpecializationCreate
) -> Specialization:
    exist = await validator.specialization_exists_by_code(
        session, specialization_create.code
    )

    if exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cпециальность с таким кодом уже существует",
        )

    exist = await validator.specialization_exists_by_title(
        session, specialization_create.title
    )

    if exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cпециальность с таким названием уже существует",
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
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return specializations


async def get_specialization(
    session: AsyncSession, id: Optional[int], code: Optional[int], title: Optional[str]
) -> Specialization:
    if not any([id, title]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Введите хотя бы один параметр: id или title.",
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


async def delete_specialization(session: AsyncSession, specialization_id: int):
    specialization = await session.get(Specialization, specialization_id)
    if not specialization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Специализация не найдена",
        )
    await session.delete(specialization)
    await session.commit()


async def get_group_count_by_specialization(
    session: AsyncSession, specialization_id: int
) -> int:
    result = await session.execute(
        select(func.count(Group.id)).where(Group.specialization_id == specialization_id)
    )
    return result.scalar_one_or_none() or 1


async def create_group(
    session: AsyncSession, group_create: GroupCreate, current_user_id: int
) -> GroupWithOutStudents:
    specialization = await get_specialization(
        session, group_create.specialization_id, None, None
    )
    group_count = await get_group_count_by_specialization(
        session, group_create.specialization_id
    )

    number = specialization.code + "-" + str(group_create.course) + str(group_count)
    if group_create.is_commeration:
        number += "K"

    if not group_create.director_id:
        group_create.director_id = current_user_id

    new_group = Group(
        number=number,
        specialization_id=group_create.specialization_id,
        course=group_create.course,
        director_id=group_create.director_id,
    )

    session.add(new_group)
    await session.commit()
    await session.refresh(new_group)

    director = await get_user_by_id(session, group_create.director_id)

    return await validator.group_to_pydantic(new_group, specialization.title, director)


async def get_groups(session: AsyncSession):
    result = await session.execute(
        select(Specialization).options(
            selectinload(Specialization.groups).selectinload(Group.director)
        )
    )

    specializations = result.scalars().all()

    if not specializations:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
        )

    specializations_data = [
        SpecializationWithGroups(
            title=spec.title,
            code=spec.code,
            groups=[
                GroupWithOutSpecialization(
                    id=group.id,
                    number=group.number,
                    course=group.course,
                    director=BaseUser(
                        id=group.director.id,
                        username=group.director.username,
                        role=group.director.role,
                        full_name=group.director.full_name,
                        group_id=group.director.group_id,
                    ),
                )
                for group in spec.groups
            ],
        )
        for spec in specializations
    ]

    return specializations_data


async def get_group_with_practices(session: AsyncSession, group_id: int) -> Group:
    result = await session.execute(
        select(Group)
        .options(
            selectinload(Group.director),
            selectinload(Group.specialization),
            selectinload(Group.practices).selectinload(Practice.creator),
        )
        .where(Group.id == group_id)
    )

    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return group
