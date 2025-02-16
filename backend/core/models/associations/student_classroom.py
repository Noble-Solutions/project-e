from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from core.models import Base
from core.models.mixins.uuid_pk import UUIDIdPkMixin


class StudentClassroomAssociation(UUIDIdPkMixin, Base):
    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "classroom_id",
            name="idx_unique_student_classroom",
        ),
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
        )
    )
    classroom_id: Mapped[int] = mapped_column(
        ForeignKey(
            "classrooms.id",
            ondelete="CASCADE",
        )
    )

    student_best_task_type: Mapped[int] = mapped_column(nullable=True)
    student_best_task_percent: Mapped[int] = mapped_column(nullable=True)

    student_worst_task_type: Mapped[int] = mapped_column(nullable=True)
    student_worst_task_percent: Mapped[int] = mapped_column(nullable=True)
