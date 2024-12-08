from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from ..user.models import Base


class Specialization(Base):
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True)
    code = Column(String(3), unique=True, nullable=False)
    title = Column(String(50), unique=True, nullable=False)

    groups = relationship(
        "Group", back_populates="specialization", cascade="all, delete-orphan"
    )


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    number = Column(String(7), unique=True, nullable=False)
    specialization_id = Column(
        Integer, ForeignKey("specializations.id"), nullable=False
    )
    course = Column(Integer, default=3, nullable=False)
    director_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    director = relationship(
        "User",
        back_populates="controlled_groups",
        foreign_keys="[Group.director_id]",
    )
    specialization = relationship("Specialization", back_populates="groups")
    students = relationship(
        "User",
        back_populates="group",
        foreign_keys="[User.group_id]",
        cascade="all, delete-orphan",
    )
    practices = relationship(
        "Practice",
        secondary="group_practice",
        back_populates="groups",
    )

    __table_args__ = (
        CheckConstraint("course >= 2 AND course <= 4", name="check_course_range"),
    )
