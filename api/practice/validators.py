from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import select, exists
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.validators import ValidateError
from .models import Practice, practice_modules


class PracticeModulesValidator:
    def __init__(
        self,
        practice_id: int,
        module_id: int,
        number: int,
        session: AsyncSession,
    ) -> None:
        self.practice_id = practice_id
        self.module_id = module_id
        self.number = number
        self.session = session

    async def validate(self):
        try:
            await self.validate_practice_id()
            await self.validate_module_id()
            await self.validate_number()
            await self.validate_unique_constraints()
        except ValidateError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    async def validate_practice_id(self):
        exists = await self._entity_exists("practices", self.practice_id)
        if not exists:
            raise ValidateError(
                f"Практика с id {self.practice_id} не найдена.",
                status.HTTP_404_NOT_FOUND,
            )

    async def validate_module_id(self):
        exists = await self._entity_exists("modules", self.module_id)
        if not exists:
            raise ValidateError(
                f"Модуль с id {self.module_id} не найден.",
                status.HTTP_404_NOT_FOUND,
            )

    async def validate_number(self):
        if not isinstance(self.number, int) or self.number <= 0:
            raise ValidateError(
                "Номер модуля должен быть положительным целым числом.",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

    async def validate_unique_constraints(self):
        query = select(1).where(
            (practice_modules.c.practice_id == self.practice_id)
            & (practice_modules.c.module_id == self.module_id)
        )
        result = await self.session.execute(query)
        if result.scalar():
            raise ValidateError(
                f"Связь практики с id {self.practice_id} и модуля с id {self.module_id} уже существует.",
                status.HTTP_409_CONFLICT,
            )

        query = select(1).where(
            (practice_modules.c.module_id == self.module_id)
            & (practice_modules.c.number == self.number)
        )
        result = await self.session.execute(query)
        if result.scalar():
            raise ValidateError(
                f"Модуль с id {self.module_id} уже привязан к номеру {self.number}.",
                status.HTTP_409_CONFLICT,
            )

    async def _entity_exists(self, table_name: str, entity_id: int) -> bool:
        query = text(f"SELECT 1 FROM {table_name} WHERE id = :id LIMIT 1")
        result = await self.session.execute(query, {"id": entity_id})
        return result.scalar() is not None


async def practice_creator_exists(
    session: AsyncSession, practice_id: int, admin_id: int
) -> bool:
    query = select(
        exists().where(
            Practice.id == practice_id,
            Practice.creator_id == admin_id,
        )
    )
    result = await session.scalar(query)
    return result


async def practice_create_validate(
    session: AsyncSession, title: str, start_at: Optional[datetime]
) -> bool:
    query = (
        select(Practice)
        .where(
            Practice.title == title,
        )
        .order_by(Practice.start_at.desc())
        .limit(1)
    )

    result = await session.execute(query)
    practice = result.scalar_one_or_none()

    if practice and start_at:
        time_difference = start_at - practice.start_at
        if time_difference < timedelta(days=335):
            return False

    return True
