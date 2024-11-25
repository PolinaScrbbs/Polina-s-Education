from typing import List
from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User, Role
from ..user.utils import role_check

from .models import LessonType


router = APIRouter(prefix="/lesson")


@router.get("s/types", response_model=List[LessonType])
async def get_types(
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN],
        "Только администраторы имеют доступ к данному ендпоинту",
    )
    return await LessonType.values()
