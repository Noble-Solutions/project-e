from typing import Optional, Self
from uuid import UUID

from pydantic import BaseModel, model_validator, ConfigDict

from core.models.task import AnswerType


class TaskCreate(BaseModel):
    text: str
    type: int
    type_of_answer: AnswerType
    correct_answer: Optional[str] = None
    points_per_task: int = 1

    @model_validator(mode="after")
    def check_answer(self) -> Self:
        if (
            self.type_of_answer == AnswerType.SHORT_ANSWER
            and self.correct_answer is None
        ):
            raise ValueError("Short answer must have correct answer")
        if (
            self.type_of_answer == AnswerType.FULL_ANSWER
            and self.correct_answer is not None
        ):
            raise ValueError("Full answer must not have correct answer")
        return self


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    text: str
    type: int
    points_per_task: int
    type_of_answer: AnswerType
    correct_answer: Optional[str]
    file_id: Optional[UUID]
    file_extension: Optional[str]
    additional_file_id: Optional[UUID]
    additional_file_extension: Optional[str]
    teacher_id: UUID


class GetAllTasksResponseModel(BaseModel):
    tasks: list[TaskRead]
