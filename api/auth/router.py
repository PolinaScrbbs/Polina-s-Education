from fastapi import Depends, APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..user.schemes import UserCreate, UserResponse
from ..database import get_session

from .schemes import LoginForm, TokenResponse
from . import queries as qr
from .validators import RegistrationValidator

router = APIRouter(prefix="/auth")


@router.post("/registration", response_class=JSONResponse)
async def create_user(
    user_create: UserCreate, session: AsyncSession = Depends(get_session)
):
    validator = RegistrationValidator(
        user_create.username,
        user_create.password,
        user_create.confirm_password,
        user_create.full_name,
        session,
    )
    await validator.validate()

    user = await qr.registration_user(session, user_create)
    return JSONResponse(
        content=UserResponse(message="Пользователь зарегестрирован", user=user).dict(),
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/login", response_class=JSONResponse)
async def get_token(
    login_form: LoginForm = Depends(LoginForm.as_form),
    session: AsyncSession = Depends(get_session),
):
    code, message, token = await qr.login(
        session, login_form.username, login_form.password
    )
    return JSONResponse(
        content=TokenResponse(message=message, access_token=token).dict(),
        status_code=code,
    )
