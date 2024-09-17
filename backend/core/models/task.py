from uuid import UUID

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base
from .mixins.uuid_pk import UUIDIdPkMixin
from enum import Enum as PyEnum


UUID_ID = UUID


class AnswerType(PyEnum):
    FULL_ANSWER = "full_answer"
    SHORT_ANSWER = "short_answer"


class Task(UUIDIdPkMixin, Base):
    type: Mapped[int]
    text: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    """
    Пока закоменчу file_id до тех пор пока мы не начнем 
    писать систему хранения файлов, будь то S3 или
    какой то другой подход
    """
    # file_id: Mapped[UUID_ID]
    type_of_answer: Mapped[AnswerType]
    teacher_id: Mapped[UUID_ID] = mapped_column(
        ForeignKey(
            "teachers.id",
            ondelete="cascade",
        )
    )
    teacher: Mapped["Teacher"] = relationship(
        "Teacher",
        back_populates="tasks",
        lazy="noload",
    )
    correct_answer: Mapped[str] = mapped_column(nullable=True)
