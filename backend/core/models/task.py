from uuid import UUID

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional

from .base import Base
from .mixins.timestamp import TimestampMixin
from .mixins.uuid_pk import UUIDIdPkMixin
from enum import Enum as PyEnum


class AnswerType(PyEnum):
    FULL_ANSWER = "full_answer"
    SHORT_ANSWER = "short_answer"


if TYPE_CHECKING:
    from .base_user import User


class Task(
    UUIDIdPkMixin,
    TimestampMixin,
    Base,
):
    type: Mapped[int]
    text: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    points_per_task: Mapped[int]
    file_id: Mapped[Optional[UUID]]
    file_extension: Mapped[Optional[str]]
    additional_file_id: Mapped[Optional[UUID]]
    additional_file_extension: Mapped[Optional[str]]
    type_of_answer: Mapped[AnswerType]
    correct_answer: Mapped[Optional[str]]

    teacher_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="cascade",
        )
    )
    teacher: Mapped["Teacher"] = relationship(
        "User",
        back_populates="tasks",
    )
