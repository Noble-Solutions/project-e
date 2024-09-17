from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.uuid_pk import UUIDIdPkMixin


class Classroom(
    UUIDIdPkMixin,
    Base,
):
    best_task_type: Mapped[int] = mapped_column(nullable=True)
    best_task_percent: Mapped[int] = mapped_column(nullable=True)

    worst_task_type: Mapped[int] = mapped_column(nullable=True)
    worst_task_percent: Mapped[int] = mapped_column(nullable=True)

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
