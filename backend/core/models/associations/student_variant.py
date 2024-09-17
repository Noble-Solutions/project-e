from uuid import uuid4

from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from core.models import Base

student_variant_association_table = Table(
    "student_variant_association",
    Base.metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    ),
    Column(
        "student_id",
        ForeignKey("students.id"),
    ),
    Column(
        "variant_id",
        ForeignKey("variants.id"),
    ),
    UniqueConstraint(
        "student_id",
        "variant_id",
        name="idx_unique_student_variant",
    ),
)
