from typing import List
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Module
from .schemes import (
    ModuleCreate,
)


async def create_module(
    session: AsyncSession, module_create: ModuleCreate, current_user_id: int
) -> Module:
    new_module = Module(
        title=module_create.title,
        description=module_create.description,
        creator_id=current_user_id,
        is_mandatory=module_create.is_mandatory,
    )

    session.add(new_module)
    await session.commit()
    await session.refresh(new_module)
    return new_module


async def get_modules(session: AsyncSession) -> List[Module]:
    result = await session.execute(
        select(Module).options(selectinload(Module.creator)).order_by(Module.title)
    )
    modules = result.scalars().all()

    if not modules:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return modules
