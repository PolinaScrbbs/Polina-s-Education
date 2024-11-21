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
