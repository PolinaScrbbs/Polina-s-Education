from datetime import datetime, timedelta
from enum import Enum as BaseEnum
import pytz
from sqlalchemy import (
    CHAR,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Enum,
    Table,
    UniqueConstraint,
)

from ..user.models import Base

practice_developers = Table(
    "practice_developers",
    Base.metadata,
    Column("practice_id", Integer, ForeignKey("practices.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    UniqueConstraint("practice_id", "user_id", name="uq_practice_developers"),
)

practice_modules = Table(
    "practice_modules",
    Base.metadata,
    Column("number", Integer, nullable=False),
    Column("practice_id", Integer, ForeignKey("practices.id"), nullable=False),
    Column("module_id", Integer, ForeignKey("modules.id"), nullable=False),
    UniqueConstraint("practice_id", "module_id", name="uq_practice_modules"),
    UniqueConstraint("module_id", "number", name="uq_module_number"),
    CheckConstraint("number > 0", name="chk_module_number_positive"),
)


class PracticeType(BaseEnum):
    EDUCATIONAL_PRACTICE = "Учебная практика"
    PRODUCTION_PRACTICE = "Производственная практика"


class Specialization(Base):
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True)
    code = Column(String(7), unique=True)
    title = Column(String(50), unique=True, nullable=False)


class PracticePattern(Base):
    __tablename__ = "practice_patterns"

    id = Column(Integer, primary_key=True)
    type = Column(
        Enum(PracticeType), default=PracticeType.EDUCATIONAL_PRACTICE, nullable=False
    )
    specialization_id = Column(
        Integer, ForeignKey("specializations.id"), nullable=False
    )
    course_number = Column(CHAR(1), default="3", nullable=False)


class Practice(Base):
    __tablename__ = "practices"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    description = Column(String(256), nullable=False)
    pattern_id = Column(Integer, ForeignKey("practice_patterns.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_at = Column(
        DateTime,
        default=lambda: datetime.now(pytz.timezone("Europe/Moscow")).replace(
            tzinfo=None
        ),
    )
    end_at = Column(
        DateTime,
        default=lambda: (
            datetime.now(pytz.timezone("Europe/Moscow")) + timedelta(weeks=1)
        ).replace(tzinfo=None),
    )
