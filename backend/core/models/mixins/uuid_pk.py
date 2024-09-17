from uuid import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

UUID_ID = UUID


class UUIDIdPkMixin:
    id: Mapped[UUID_ID] = mapped_column(primary_key=True, nullable=False)
