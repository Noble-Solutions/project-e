from uuid import uuid4

from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from core.models import Base

variant_task_association_table = Table(
    "variant_task_association",
    Base.metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        default=uuid4,
        primary_key=True,
    ),
    Column(
        "variant_id",
        ForeignKey("variants.id"),
    ),
    Column(
        "task_id",
        ForeignKey("tasks.id"),
    ),
    UniqueConstraint(
        "variant_id",
        "task_id",
        name="idx_unique_variant_task",
    ),
)
