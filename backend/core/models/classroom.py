from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.uuid_pk import UUIDIdPkMixin
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .user_roles import Teacher, Student


class Classroom(
    UUIDIdPkMixin,
    Base,
):
    name: Mapped[str]
    subject: Mapped[str]
    amount_of_students: Mapped[int]
    best_task_type: Mapped[Optional[int]]
    best_task_percent: Mapped[Optional[int]]
    worst_task_type: Mapped[Optional[int]]
    worst_task_percent: Mapped[Optional[int]]

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey(
            "teachers.id",
            ondelete="cascade",
        )
    )
    teacher: Mapped["Teacher"] = relationship(
        "Teacher",
        back_populates="classrooms",
    )
    students: Mapped[list["Student"]] = relationship(
        back_populates="classrooms",
        secondary="student_classroom_associations",
    )
