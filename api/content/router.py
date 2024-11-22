from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User, Role
from ..user.utils import role_check

from . import queries as qr
from .schemes import ContentCreate, ContentWithoutCreator

router = APIRouter(prefix="/content")


@router.post(
    "", response_model=ContentWithoutCreator, status_code=status.HTTP_201_CREATED
)
async def create_content(
    content_create: ContentCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await role_check(
        current_user,
        [Role.ADMIN],
        "Только администратор имеет доступ к данному эндпоинту",
    )
    new_content = await qr.create_content(session, content_create, current_user.id)
    return new_content
