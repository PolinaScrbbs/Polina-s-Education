from datetime import datetime
import pytz
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)

from ..practice.models import Base

module_lessons = Table(
    "module_lessons",
    Base.metadata,
    Column("number", Integer, nullable=False),
    Column("module_id", Integer, ForeignKey("modules.id"), nullable=False),
    Column("lesson_id", Integer, ForeignKey("lessons.id"), nullable=False),
    UniqueConstraint("module_id", "lesson_id", name="uq_module_lessons"),
    UniqueConstraint("lesson_id", "number", name="uq_lesson_number"),
    CheckConstraint("number > 0", name="chk_lesson_number_positive"),
)


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    description = Column(String(256), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_mandatory = Column(Boolean, default=True, nullable=False)


class ModuleResult(Base):
    __tablename__ = "module_results"

    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    completed_lessons_count = Column(Integer, default=0, nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(pytz.timezone("Europe/Moscow")).replace(
            tzinfo=None
        ),
    )
    UniqueConstraint("module_id", "student_id", name="uq_student_module_result")
    CheckConstraint(
        "completed_lessons_count > 0", name="chk_completed_lessons_count_positive"
    )
