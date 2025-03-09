from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Path, Depends

from core.schemas.user import AccessTokenPayload
from core.services.analytics import AnalyticsService
from core.services.get_service import get_service
from core.utils.auth_utils import get_current_teacher

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@router.get("/student/{student_id}/classroom/{classroom_id}/")
async def get_analytics(
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    student_id: Annotated[UUID, Path],
    classroom_id: Annotated[UUID, Path],
    analytics_service: Annotated[
        "AnalyticsService",
        Depends(get_service(AnalyticsService)),
    ],
):
    return await analytics_service.get_performance_of_student_in_classroom(
        student_id=student_id,
        classroom_id=classroom_id,
    )
