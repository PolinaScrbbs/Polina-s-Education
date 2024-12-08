from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from ..user.models import User
from .models import Group, Specialization
from .schemes import GroupWithOutStudents, BaseUser


async def specialization_exists_by_code(
    session: AsyncSession, code: str = None
) -> bool:
    query = select(exists().where(Specialization.code == code))
    result = await session.scalar(query)
    return result


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


async def group_to_pydantic(
    group: Group, specialization: str, director: User
) -> GroupWithOutStudents:
    director = BaseUser(
        id=director.id,
        username=director.username,
        role=director.role,
        full_name=director.full_name,
        group_id=director.group_id,
    )

    return GroupWithOutStudents(
        id=group.id,
        number=group.number,
        specialization=specialization,
        course=group.course,
        director=director,
    )
