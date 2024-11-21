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
    GetPracticePatternsFilters,
    PracticeCreate,
    PracticeWitoutCreator,
    PracticeInDB,
    GetPracticeFilters,
)

router = APIRouter(prefix="/practice")


@router.post(
    "s/specialization",
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


@router.get("s/specializations", response_model=List[SpecializationInDB])
async def get_specializations(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    specializations = await qr.get_specializations(session)
    return specializations


@router.get("s/specialization", response_model=SpecializationInDB)
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
    "s/pattern", response_model=PracticePatternInDB, status_code=status.HTTP_201_CREATED
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


@router.get("s/patterns", response_model=List[PracticePatternInDB])
async def get_practice_patterns(
    filters: GetPracticePatternsFilters = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await admin_check(current_user)
    practice_patterns = await qr.get_practice_patterns(session, filters)
    return practice_patterns


@router.get("s/pattern", response_model=PracticePatternInDB)
async def get_practice_pattern_by_id(
    practice_pattern_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await admin_check(current_user)
    practice_pattern = await qr.get_practice_pattern_by_id(session, practice_pattern_id)
    return practice_pattern


@router.post(
    "",
    response_model=PracticeWitoutCreator,
    status_code=status.HTTP_201_CREATED,
)
async def create_practice(
    practice_create: PracticeCreate = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await admin_check(current_user)
    new_practice = await qr.create_practice(session, practice_create, current_user.id)
    return new_practice


@router.get("s", response_model=List[PracticeInDB])
async def get_practices(
    filters: GetPracticeFilters = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    practices = await qr.get_practices(session, filters)
    return practices


@router.get("", response_model=PracticeInDB)
async def get_practice_by_id(
    practice_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    practice = await qr.get_practice_by_id(session, practice_id)
    return practice
