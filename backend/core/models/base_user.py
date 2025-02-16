from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base

from .mixins.uuid_pk import UUIDIdPkMixin
from typing import Literal, Optional

RoleType = Literal["teacher", "student"]

Subject = Literal[
    "informatics",
    "math",
    "russian",
    "english",
    "french",
    "spanish",
    "german",
    "history",
    "social_studies",
    "geography",
    "biology",
    "chemistry",
    "physics",
]


class User(UUIDIdPkMixin, Base):
    # username также используется как login
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[bytes]
    first_name: Mapped[str]
    last_name: Mapped[str]
    role_type: Mapped[RoleType]
    subject: Mapped[Optional[Subject]]

    # Teacher relationships
    variants: Mapped[list["Variant"]] = relationship(
        back_populates="teacher",
    )
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="teacher",
    )
    classrooms: Mapped[list["Classroom"]] = relationship(
        back_populates="teacher",
    )

    # Student relationships
    classrooms_of_student: Mapped[list["Classroom"]] = relationship(
        back_populates="students",
        secondary="student_classroom_associations",
    )

    variants_of_student: Mapped[list["Variant"]] = relationship(
        back_populates="students",
        secondary="student_variant_associations",
    )
