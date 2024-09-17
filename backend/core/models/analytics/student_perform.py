"""
Здесь будет модель для записи в бд
статистики студента по каждому заданию в определенном классе
"""

from core.models.base import Base
from core.models.mixins.uuid_pk import UUIDIdPkMixin
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class StudentPerformance(UUIDIdPkMixin, Base):
    __tablename__ = "students_performance"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "classroom_id",
            "task_type",
            name="idx_unique_student_classroom_task_type",
        ),
    )

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    task_type: Mapped[int]
    total_solved: Mapped[int]
    correct_solved: Mapped[int]
