from enum import Enum as BaseEnum
from typing import Optional
import jwt
import bcrypt
import pytz
from datetime import datetime, timedelta
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from config import SECRET_KEY
from ..database import Base


class Role(BaseEnum):
    ADMIN = "Администратор"
    TEACHER = "Преподаватель"
    STUDENT = "Студент"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    hashed_password = Column(String(512), nullable=False)
    full_name = Column(String(50), nullable=False)
    role = Column(Enum(Role), default=Role.STUDENT, nullable=False)

    async def set_password(self, password: str) -> None:
        self.hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    async def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), self.hashed_password.encode("utf-8")
        )

    async def generate_token(self, expires_in: int = 4800) -> str:
        payload = {
            "user_id": self.id,
            "exp": datetime.now(pytz.timezone("Europe/Moscow"))
            + timedelta(seconds=expires_in),
        }
        print(f"SECRET_KEY: {SECRET_KEY} (type: {type(SECRET_KEY)})")
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String(256), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    async def verify_token(self, session: AsyncSession, user: Optional[User]):
        try:
            jwt.decode(self.token, SECRET_KEY, algorithms=["HS256"])
            return status.HTTP_200_OK, "Токен верефицирован", self

        except jwt.ExpiredSignatureError:
            return await self.refresh_token(session, user)

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неправильный токен",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def refresh_token(self, session: AsyncSession, user: Optional[User]):
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен истёк",
                headers={"WWW-Authenticate": "Bearer"},
            )

        new_token = await user.generate_token()

        self.token = new_token
        session.add(self)
        await session.commit()

        return status.HTTP_200_OK, "Токен обновлён", self
