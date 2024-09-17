from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins.uuid_pk import UUIDIdPkMixin


class VariantTaskAssociation(UUIDIdPkMixin, Base):
    __table_args__ = (
        UniqueConstraint(
            "variant_id",
            "task_id",
            name="idx_unique_variant_task",
        ),
    )

    variant_id: Mapped[int] = mapped_column(ForeignKey("variants.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
