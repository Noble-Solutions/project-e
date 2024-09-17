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

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    variant_id: Mapped[int] = mapped_column(ForeignKey("variants.id"))
