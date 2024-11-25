from datetime import datetime
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
from sqlalchemy.orm import relationship

from ..content.models import Base
from ..user.models import BaseEnum

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

    results = relationship(
        "LessonResult", back_populates="lesson", cascade="all, delete-orphan"
    )


class LessonResultStatus(BaseEnum):
    SENT = "Отправлено"
    VIEWED = "Просмотрено"
    SENT_FOR_REVISION = "Отправлено на доработку"
    APPRECIATED = "Оценено"


class LessonResult(Base):
    __tablename__ = "lesson_results"

    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
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

    lesson = relationship("Lesson", back_populates="results")


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
