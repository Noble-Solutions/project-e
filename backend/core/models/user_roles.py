from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from .base_user import User
from uuid import UUID

UUID_ID = UUID

if TYPE_CHECKING:
    from .variant import Variant


class Teacher(User):
    id: Mapped[UUID_ID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    subject: Mapped[str]
    variants: Mapped[list["Variant"]] = relationship(
        back_populates="teacher",
    )
    mapper_args = {
        "polymorphic_identity": "teacher",
    }


# Student model inheriting from User
class Student(User):
    id: Mapped[UUID_ID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    mapper_args = {
        "polymorphic_identity": "student",
    }
