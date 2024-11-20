from typing import List, Optional
from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User
from ..user.utils import admin_check

from . import queries as qr
from .schemes import (
    SpecializationCreate,
    SpecializationInDB,
    PracticePatternCreate,
    PracticePatternInDB,
)

router = APIRouter(prefix="/practices")


@router.post(
    "/specialization",
    response_model=SpecializationInDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_specialization(
    specialization_create: SpecializationCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await admin_check(current_user)
    new_specialization = await qr.create_specialization(session, specialization_create)
    return new_specialization


@router.get("/specializations", response_model=List[SpecializationInDB])
async def get_specializations(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    specializations = await qr.get_specializations(session)
    return specializations


@router.get("/specialization", response_model=SpecializationInDB)
async def get_specialization(
    id: Optional[int] = None,
    code: Optional[str] = None,
    title: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    specialization = await qr.get_specialization(session, id, code, title)
    return specialization


@router.post(
    "/pattern", response_model=PracticePatternInDB, status_code=status.HTTP_201_CREATED
)
async def create_practice_pattern(
    practice_patteren_create: PracticePatternCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await admin_check(current_user)
    new_practice_pattern = await qr.create_practice_pattern(
        session, practice_patteren_create
    )
    return new_practice_pattern


@router.get("/patterns", response_model=List[PracticePatternInDB])
async def get_practice_patterns(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await admin_check(current_user)
    practice_patterns = await qr.get_practice_patterns(session)
    return practice_patterns
