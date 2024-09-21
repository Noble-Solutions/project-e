from pydantic import BaseModel, Field, ConfigDict
from backend_types import RoleType
from typing import Annotated, Optional


class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=5, max_length=20)]
    password: str
    first_name: str
    last_name: str
    role_type: RoleType


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    first_name: str
    last_name: str
    role_type: RoleType


class TeacherRead(UserRead):
    subject: Annotated[Optional[str], Field(default=None)]


class StudentRead(UserRead):
    pass


class UserCreateInDB(UserCreate):
    password: str = Field(exclude=True, default=None)
    hashed_password: bytes
