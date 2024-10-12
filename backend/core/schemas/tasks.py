from typing import Optional, Self
from uuid import UUID

from pydantic import BaseModel, model_validator, ConfigDict

from core.models.task import AnswerType


class TaskCreate(BaseModel):
    text: str
    type: int
    type_of_answer: AnswerType
    correct_answer: Optional[str] = None

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
    type_of_answer: AnswerType
    correct_answer: Optional[str]
    file_id: Optional[UUID]
    teacher_id: Optional[UUID]
