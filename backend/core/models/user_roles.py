from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_user import User
from uuid import UUID

UUID_ID = UUID

if TYPE_CHECKING:
    from .variant import Variant
    from .task import Task
    from .classroom import Classroom


class Teacher(User):
    id: Mapped[UUID_ID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    subject: Mapped[str]
    variants: Mapped[list["Variant"]] = relationship(
        back_populates="teacher",
    )
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="teacher",
    )
    classrooms: Mapped[list["Classroom"]] = relationship(
        back_populates="teacher",
    )
    mapper_args = {
        "polymorphic_identity": "teacher",
    }


# Student model inheriting from User
class Student(User):
    id: Mapped[UUID_ID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    variants: Mapped[list["Variant"]] = relationship(
        back_populates="students",
        secondary="student_variant_associations",
    )
    classrooms: Mapped[list["Classroom"]] = relationship(
        back_populates="students",
        secondary="student_classroom_associations",
    )
    mapper_args = {
        "polymorphic_identity": "student",
    }
