from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Path
from starlette import status

from core.schemas.analytics import TaskStatCreate
from core.schemas.response_models.variant import (
    GetVariantByIDWithTasksResponse,
    GetAllVariantsResponse,
    CheckVariantResponse,
)
from core.schemas.variant import VariantCreate, VariantRead
from core.schemas.user import AccessTokenPayload
from core.services.analytics import AnalyticsService
from core.services.get_service import get_service
from core.services.variants import VariantsService
from core.utils.auth_utils import (
    get_current_user,
    get_current_teacher,
    get_current_student,
)

router = APIRouter(
    prefix="/variants",
    tags=["variants"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=GetAllVariantsResponse,
)
async def get_all_variants_of_user(
    user: Annotated[
        "AccessTokenPayload",
        Depends(get_current_user),
    ],
    variants_service: Annotated[
        "VariantsService",
        Depends(get_service(VariantsService)),
    ],
):
    return await variants_service.get_all_variants_of_user(
        user_id=user.id,
        user_role=user.role_type,
    )


@router.get(
    "/{variant_id}/",
    status_code=status.HTTP_200_OK,
    response_model=GetVariantByIDWithTasksResponse,
)
async def get_variant_by_id_with_tasks(
    user: Annotated[
        "AccessTokenPayload",
        Depends(get_current_user),
    ],
    variant_id: Annotated[UUID, Path],
    variants_service: Annotated[
        "VariantsService",
        Depends(get_service(VariantsService)),
    ],
):
    return await variants_service.get_variant_by_id_with_tasks(
        variant_id=variant_id,
        user_id=user.id,
        user_role=user.role_type,
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=VariantRead,
)
async def create_variant(
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    variant_create: VariantCreate,
    variants_service: Annotated[
        "VariantsService",
        Depends(get_service(VariantsService)),
    ],
):

    return await variants_service.create_variant(
        variant_create=variant_create,
        teacher_id=teacher.id,
    )


@router.put(
    "/{variant_id}/",
    status_code=status.HTTP_200_OK,
    response_model=VariantRead,
)
async def update_variant(
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    variant_id: Annotated[UUID, Path],
    variant_update: VariantCreate,
    variants_service: Annotated[
        "VariantsService",
        Depends(get_service(VariantsService)),
    ],
):
    return await variants_service.update_variant(
        variant_id=variant_id,
        variant_update=variant_update,
        teacher_id=teacher.id,
    )


@router.delete("/{variant_id}/", status_code=status.HTTP_200_OK)
async def delete_variant(
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    variant_id: Annotated[UUID, Path],
    variants_service: Annotated[
        "VariantsService",
        Depends(get_service(VariantsService)),
    ],
):
    return await variants_service.delete_variant(
        variant_id=variant_id,
        teacher_id=teacher.id,
    )


@router.post("/add_task/{variant_id}/task/{task_id}", status_code=status.HTTP_200_OK)
async def add_task_to_variant(
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    variant_id: Annotated[UUID, Path],
    task_id: Annotated[UUID, Path],
    variants_service: Annotated[
        "VariantsService",
        Depends(get_service(VariantsService)),
    ],
):
    return await variants_service.add_task_to_variant(
        variant_id=variant_id,
        task_id=task_id,
        teacher_id=teacher.id,
    )


@router.delete(
    "/remove_task/{variant_id}/task/{task_id}",
    status_code=status.HTTP_200_OK,
)
async def remove_task_from_variant(
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    variant_id: Annotated[UUID, Path],
    task_id: Annotated[UUID, Path],
    variants_service: Annotated[
        "VariantsService",
        Depends(get_service(VariantsService)),
    ],
):
    return await variants_service.remove_task_from_variant(
        variant_id=variant_id,
        task_id=task_id,
        teacher_id=teacher.id,
    )


@router.post(
    "/check/{variant_id}",
    status_code=status.HTTP_200_OK,
    response_model=CheckVariantResponse,
)
async def check_variant(
    variant_id: Annotated[UUID, Path],
    classroom_id: UUID,
    task_id_to_answer: dict[UUID, str | int],
    variants_service: Annotated[
        "VariantsService",
        Depends(get_service(VariantsService)),
    ],
    analytics_service: Annotated[
        "AnalyticsService",
        Depends(get_service(AnalyticsService)),
    ],
    student: Annotated[
        "AccessTokenPayload",
        Depends(get_current_student),
    ],
):
    checked_variant = await variants_service.check_variant(
        variant_id=variant_id,
        task_id_to_answer=task_id_to_answer,
    )

    for task_type, task_stats in checked_variant.get(
        "task_stats_for_analytics"
    ).items():
        await analytics_service.add_task_result(
            task_stat_create=TaskStatCreate(
                student_id=student.id,
                classroom_id=classroom_id,
                task_type=task_type,
                correct_solved=task_stats[0],
                total_solved=task_stats[1],
            )
        )
    return {
        "maximum_points": checked_variant.get("maximum_points"),
        "points_earned_by_student": checked_variant.get("points_earned_by_student"),
    }


@router.post(
    "/assign_to_student/{variant_id}/{student_id}/{classroom_id}",
    status_code=status.HTTP_200_OK,
)
async def assign_variant_to_student(
    variant_id: Annotated[UUID, Path],
    student_id: Annotated[UUID, Path],
    classroom_id: Annotated[UUID, Path],
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    variants_service: Annotated[
        "VariantsService",
        Depends(get_service(VariantsService)),
    ],
):
    await variants_service.assign_variant_to_student(
        variant_id=variant_id,
        student_id=student_id,
        teacher_id=teacher.id,
        classroom_id=classroom_id,
    )

    return {"status": "ok"}


@router.post(
    "/assign_to_classroom/{variant_id}/{classroom_id}", status_code=status.HTTP_200_OK
)
async def assign_variant_to_all_students_in_classroom(
    variant_id: Annotated[UUID, Path],
    classroom_id: Annotated[UUID, Path],
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    variants_service: Annotated[
        "VariantsService",
        Depends(get_service(VariantsService)),
    ],
):
    await variants_service.assign_variant_to_all_students_in_classroom(
        variant_id=variant_id,
        classroom_id=classroom_id,
        teacher_id=teacher.id,
    )
    return {"status": "ok"}
