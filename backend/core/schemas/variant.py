from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VariantCreate(BaseModel):
    name: str


class VariantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    subject: str
    amount_of_tasks: int
    maximum_score_from_short_answer_task: int
    teacher_id: UUID
