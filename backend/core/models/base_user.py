from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base

from .mixins.uuid_pk import UUIDIdPkMixin
from backend_types import RoleType


class User(UUIDIdPkMixin, Base):
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[bytes]
    first_name: Mapped[str]
    last_name: Mapped[str]
    role_type: Mapped[RoleType]

    mapper_args = {
        "polymorphic_on": "role_type",
        "polymorphic_identity": "user",
    }
