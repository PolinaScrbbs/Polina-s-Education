from datetime import datetime, timedelta
from enum import Enum as BaseEnum
import pytz
from sqlalchemy import CheckConstraint, CHAR, Column, DateTime, ForeignKey, Integer, String, Enum, Table, UniqueConstraint

from ..practice.models import Base

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    description = Column(String(256), nullable=False)

class ModuleResult(Base):
    __tablename__ = "module_results"

    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    completed_lessons_count = Column(Integer, default=0, nullable=False)
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(pytz.timezone("Europe/Moscow")).replace(tzinfo=None)
    )
    UniqueConstraint("module_id", "student_id", name="uq_student_module_result")
    CheckConstraint("completed_lessons_count > 0", name="chk_completed_lessons_count_positive")