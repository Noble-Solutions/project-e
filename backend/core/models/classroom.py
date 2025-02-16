from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.uuid_pk import UUIDIdPkMixin
from .mixins.timestamp import TimestampMixin
from typing import TYPE_CHECKING, Optional
from .base_user import Subject

if TYPE_CHECKING:
    from .base_user import User


class Classroom(
    UUIDIdPkMixin,
    TimestampMixin,
    Base,
):
    name: Mapped[str]
    subject: Mapped[Subject]
    amount_of_students: Mapped[int]
    best_task_type: Mapped[Optional[int]]
    best_task_percent: Mapped[Optional[int]]
    worst_task_type: Mapped[Optional[int]]
    worst_task_percent: Mapped[Optional[int]]

    teacher_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="cascade",
        )
    )
    teacher: Mapped["User"] = relationship(
        "User",
        back_populates="classrooms",
    )
    students: Mapped[list["User"]] = relationship(
        back_populates="classrooms_of_student",
        secondary="student_classroom_associations",
    )
