from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TaskStatCreate(BaseModel):
    student_id: UUID
    classroom_id: UUID
    task_type: int
    correct_solved: int
    total_solved: int


class TaskStatRead(TaskStatCreate):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
