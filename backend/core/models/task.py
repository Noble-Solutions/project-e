from uuid import UUID

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional

from .base import Base
from .mixins.uuid_pk import UUIDIdPkMixin
from enum import Enum as PyEnum


UUID_ID = UUID


class AnswerType(PyEnum):
    FULL_ANSWER = "full_answer"
    SHORT_ANSWER = "short_answer"


if TYPE_CHECKING:
    from .user_roles import Teacher


class Task(
    UUIDIdPkMixin,
    Base,
):
    type: Mapped[int]
    text: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    file_id: Mapped[Optional[UUID_ID]]
    type_of_answer: Mapped[AnswerType]
    correct_answer: Mapped[Optional[str]]

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey(
            "teachers.id",
            ondelete="cascade",
        )
    )
    teacher: Mapped["Teacher"] = relationship(
        "Teacher",
        back_populates="tasks",
    )
