from typing import Optional
from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User
from ..user.utils import admin_check

from . import queries as qr
from .schemes import SpecializationCreate, SpecializationInDB

router = APIRouter(prefix="/practices")


@router.post("", response_model=SpecializationInDB, status_code=status.HTTP_201_CREATED)
async def create_specialization(
    specialization_create: SpecializationCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await admin_check(current_user)
    new_specialization = await qr.create_specialization(session, specialization_create)
    return new_specialization
