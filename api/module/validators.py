from fastapi import HTTPException, status
from sqlalchemy import select, exists
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.validators import ValidateError
from .models import Module, ModuleResult, module_lessons


class ModuleLessonsValidator:
    def __init__(
        self,
        module_id: int,
        lesson_id: int,
        number: int,
        session: AsyncSession,
    ) -> None:
        self.module_id = module_id
        self.lesson_id = lesson_id
        self.number = number
        self.session = session

    async def validate(self):
        try:
            await self.validate_module_id()
            await self.validate_lesson_id()
            await self.validate_number()
            await self.validate_unique_constraints()
        except ValidateError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    async def validate_module_id(self):
        exists = await self._entity_exists("modules", self.module_id)
        if not exists:
            raise ValidateError(
                f"Модуль с id {self.module_id} не найден.",
                status.HTTP_404_NOT_FOUND,
            )

    async def validate_lesson_id(self):
        exists = await self._entity_exists("lessons", self.lesson_id)
        if not exists:
            raise ValidateError(
                f"Урок с id {self.lesson_id} не найден.",
                status.HTTP_404_NOT_FOUND,
            )

    async def validate_number(self):
        if not isinstance(self.number, int) or self.number <= 0:
            raise ValidateError(
                "Номер урока должен быть положительным целым числом.",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

    async def validate_unique_constraints(self):
        query = select(module_lessons).where(
            (module_lessons.c.module_id == self.module_id)
            & (module_lessons.c.lesson_id == self.lesson_id)
        )
        result = await self.session.execute(query)
        if result.scalar():
            raise ValidateError(
                f"Связь модуля с id {self.module_id} и урока с id {self.lesson_id} уже существует.",
                status.HTTP_409_CONFLICT,
            )

        query = select(module_lessons).where(
            (module_lessons.c.lesson_id == self.lesson_id)
            & (module_lessons.c.number == self.number)
        )
        result = await self.session.execute(query)
        if result.scalar():
            raise ValidateError(
                f"Урок с id {self.lesson_id} уже привязан к номеру {self.number}.",
                status.HTTP_409_CONFLICT,
            )

    async def _entity_exists(self, table_name: str, entity_id: int) -> bool:
        query = text(f"SELECT 1 FROM {table_name} WHERE id = :id LIMIT 1")
        result = await self.session.execute(query, {"id": entity_id})
        return result.scalar() is not None


async def module_creator_exists(session: int, module_id: int, teacher_id: int) -> bool:
    query = select(
        exists().where(
            Module.id == module_id,
            Module.creator_id == teacher_id,
        )
    )
    result = await session.scalar(query)
    return result


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


async def student_module_result_exists(
    session: AsyncSession, module_result_id: int, student_id: int
) -> bool:
    query = select(
        exists().where(
            ModuleResult.id == module_result_id,
            ModuleResult.student_id == student_id,
        )
    )
    result = await session.scalar(query)
    return result
