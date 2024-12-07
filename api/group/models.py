from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    UniqueConstraint,
    CheckConstraint,
)
from ..user.models import Base


class Specialization(Base):
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True, nullable=False)


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    number = Column(String(7), unique=True, nullable=False)
    specialization_id = Column(
        Integer, ForeignKey("specializations.id"), nullable=False
    )
    course = Column(Integer, default=3, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "specialization_id", "course", name="unique_specialization_course"
        ),
        CheckConstraint("course >= 2 AND course <= 4", name="check_course_range"),
    )
