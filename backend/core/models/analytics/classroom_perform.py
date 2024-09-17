"""
Здесь будет модель для хранения в бд статистики класса
по определенному типу задания
"""

from core.models.base import Base
from core.models.mixins.uuid_pk import UUIDIdPkMixin
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ClassRoomPerformance(UUIDIdPkMixin, Base):
    __tablename__ = "classrooms_performance"

    __table_args__ = (
        UniqueConstraint(
            "classroom_id",
            "task_type",
            name="idx_unique_classroom_task_type",
        ),
    )

    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    task_type: Mapped[int]
    total_solved: Mapped[int]
    correct_solved: Mapped[int]
