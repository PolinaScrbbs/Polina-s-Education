from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User
from ..user.utils import admin_check

from . import queries as qr
from .schemes import ModuleCreate, ModuleWithoutCreator

router = APIRouter(prefix="/module")


@router.post(
    "", response_model=ModuleWithoutCreator, status_code=status.HTTP_201_CREATED
)
async def create_module(
    module_create: ModuleCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await admin_check(current_user)
    new_module = await qr.create_module(session, module_create, current_user.id)
    return new_module
