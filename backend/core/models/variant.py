from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from core.models.base import Base
from .mixins.uuid_pk import UUIDIdPkMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task
    from .user_roles import Student, Teacher


class Variant(
    UUIDIdPkMixin,
    Base,
):
    students: Mapped[list["Student"]] = relationship(
        back_populates="variants",
        secondary="student_variant_associations",
    )
    tasks: Mapped[list["Task"]] = relationship(
        secondary="variant_task_associations",
    )
    total_tasks: Mapped[int]
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey(
            "teachers.id",
            ondelete="cascade",
        )
    )
    teacher: Mapped["Teacher"] = relationship(
        "Teacher",
        back_populates="variants",
    )
