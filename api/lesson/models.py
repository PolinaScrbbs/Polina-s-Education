from datetime import datetime
from enum import Enum as BaseEnum
import pytz
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Enum,
    Table,
    UniqueConstraint,
)

from ..module.models import Base

lesson_contents = Table(
    "lesson_contents",
    Base.metadata,
    Column("lesson_id", Integer, ForeignKey("lessons.id")),
    Column("content_id", Integer, ForeignKey("contents.id")),
    UniqueConstraint("lesson_id", "content_id", name="uq_lesson_content"),
)

lesson_result_contents = Table(
    "lesson_result_contents",
    Base.metadata,
    Column("lesson_result_id", Integer, ForeignKey("lesson_results.id")),
    Column("content_id", Integer, ForeignKey("contents.id")),
    UniqueConstraint("lesson_result_id", "content_id", name="uq_lesson_result_content"),
)


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    description = Column(String(256), nullable=False)
    file_path = Column(String(128), unique=True, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(pytz.timezone("Europe/Moscow")).replace(
            tzinfo=None
        ),
    )
    last_updated_at = Column(DateTime, default=None)


class LessonType(BaseEnum):
    THEORY = "Теория"
    TEST = "Тест"
    PRACTICE = "Практика"


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    description = Column(String(256), nullable=False)
    type = Column(Enum(LessonType), default=LessonType.PRACTICE, nullable=False)


class LessonResultStatus(BaseEnum):
    SENT = "Отправлено"
    VIEWED = "Просмотрено"
    SENT_FOR_REVISION = "Отправлено на доработку"
    APPRECIATED = "Оценено"


class LessonResult(Base):
    __tablename__ = "lesson_results"

    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    status = Column(
        Enum(LessonResultStatus), default=LessonResultStatus.SENT, nullable=False
    )
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(pytz.timezone("Europe/Moscow")).replace(
            tzinfo=None
        ),
    )
    last_updated_at = Column(DateTime, default=None)
    UniqueConstraint("lesson_id", "student_id", name="uq_student_lesson_result")


class LessonResultEvaluation(Base):
    __tablename__ = "lesson_result_evaluations"

    id = Column(Integer, primary_key=True)
    lesson_result_id = Column(
        Integer, ForeignKey("lesson_results.id"), unique=True, nullable=False
    )
    evaluation = Column(Integer, default=5, nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(pytz.timezone("Europe/Moscow")).replace(
            tzinfo=None
        ),
    )
