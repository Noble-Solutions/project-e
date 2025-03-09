from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins.uuid_pk import UUIDIdPkMixin


class StudentVariantAssociation(UUIDIdPkMixin, Base):
    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "variant_id",
            name="idx_unique_student_variant",
        ),
    )
    classroom_id: Mapped[UUID]
    student_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    variant_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "variants.id",
            ondelete="CASCADE",
        )
    )
