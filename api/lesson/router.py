from typing import List
from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User, Role
from ..user.utils import role_check

from .models import LessonType
from . import queries as qr
from .schemes import LessonCreate, LessonInDB, GetLessonFilters


router = APIRouter(prefix="/lesson")


@router.get("s/types", response_model=List[LessonType])
async def get_types(
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN, Role.TEACHER],
        "Студенты не имеют доступа к данному ендпоинту",
    )
    return await LessonType.values()


@router.post("", response_model=LessonInDB, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    lesson_create: LessonCreate = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN, Role.TEACHER],
        "Студенты не имеют доступа к данному ендпоинту",
    )

    new_lesson = await qr.create_lesson(session, lesson_create)
    return new_lesson


@router.get("s", response_model=List[LessonInDB])
async def get_lessons(
    filters: GetLessonFilters = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN, Role.TEACHER],
        "Студенты не имеют доступа к данному ендпоинту",
    )

    lessons = await qr.get_lessons(session, filters)
    return lessons
