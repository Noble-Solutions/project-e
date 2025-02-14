from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, model_validator
from backend_types import RoleType
from typing import Annotated, Optional, Self

from core.models.base_user import Subject
from core.utils.exceptions import invalid_data_for_register_exc


class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=5, max_length=20)]
    password: str
    first_name: str
    last_name: str
    role_type: RoleType
    subject: Optional[Subject] = Field(None)

    @model_validator(mode="after")
    def check_subject(self) -> Self:
        if self.role_type == "teacher" and self.subject is None:
            raise invalid_data_for_register_exc
        if self.role_type == "student" and self.subject is not None:
            raise invalid_data_for_register_exc
        return self


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    username: str
    first_name: str
    last_name: str
    role_type: RoleType
    subject: Optional[Subject]


class AccessTokenPayload(BaseModel):
    id: UUID
    username: str
    role_type: RoleType
    subject: Optional[Subject]


class UserCreateInDB(UserCreate):
    password: str = Field(exclude=True, default=None)
    hashed_password: bytes
