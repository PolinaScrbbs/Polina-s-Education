from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ModuleResult


async def module_result_exists(
    session: AsyncSession, module_id: int, student_id: int
) -> bool:
    query = select(
        exists().where(
            ModuleResult.module_id == module_id,
            ModuleResult.student_id == student_id,
        )
    )
    result = await session.scalar(query)
    return result
