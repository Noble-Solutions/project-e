from uuid import UUID

from pydantic import BaseModel

from core.schemas.tasks import TaskRead
from core.schemas.variant import VariantRead


class GetAllVariantsResponse(BaseModel):
    variants: list[VariantRead]


class VariantReadAndTaskRead(BaseModel):
    variant_data: VariantRead
    tasks: list[TaskRead]


class GetVariantByIDWithTasksResponse(BaseModel):
    variant: VariantReadAndTaskRead


class CheckVariantResponse(BaseModel):
    maximum_points: int
    points_earned_by_student: int
