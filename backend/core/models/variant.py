from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from .mixins.uuid_pk import UUIDIdPkMixin
from typing import TYPE_CHECKING

UUID_ID = UUID

if TYPE_CHECKING:
    from .user_roles import Teacher


class Variant(UUIDIdPkMixin, Base):
    teacher_id: Mapped[UUID_ID] = mapped_column(
        ForeignKey(
            "teachers.id",
            ondelete="cascade",
        )
    )
    teacher: Mapped["Teacher"] = relationship(
        "Teacher",
        back_populates="variants",
        lazy="noload",
    )
