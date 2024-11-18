from sqlalchemy import Column, Integer, String, Enum
from enum import Enum as BaseEnum

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
