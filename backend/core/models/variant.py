from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from core.models.base import Base
from .mixins.uuid_pk import UUIDIdPkMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task
    from .base_user import User


class Variant(
    UUIDIdPkMixin,
    Base,
):
    name: Mapped[str]
    subject: Mapped[str]
    amount_of_tasks: Mapped[int]
    maximum_score_from_short_answer_task: Mapped[int]
    teacher_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="cascade",
        )
    )

    teacher: Mapped["Teacher"] = relationship(
        "User",
        back_populates="variants",
    )

    students: Mapped[list["User"]] = relationship(
        back_populates="variants_of_student",
        secondary="student_variant_associations",
    )

    tasks: Mapped[list["Task"]] = relationship(
        secondary="variant_task_associations",
    )
