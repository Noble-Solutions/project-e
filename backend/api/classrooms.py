from uuid import UUID

from fastapi import APIRouter, Depends
from typing import Annotated

from core.schemas import ClassroomCreate
from core.schemas.user import AccessTokenPayload
from core.services.get_service import get_service
from core.utils.auth_utils import get_current_teacher
from core.services.classrooms import ClassroomsService

router = APIRouter(
    prefix="/classrooms",
    tags=["classrooms"],
)


@router.get("/get_all_classrooms_of_teacher")
async def get_all_classrooms_of_teacher(
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    classroom_service: Annotated[
        "ClassroomsService",
        Depends(get_service(ClassroomsService)),
    ],
):
    return await classroom_service.get_all_classrooms_of_teacher(teacher.id)


@router.get("/get_classroom_by_id_with_students")
async def get_classroom_by_id_with_students(
    classroom_id: UUID,
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    classroom_service: Annotated[
        "ClassroomsService",
        Depends(get_service(ClassroomsService)),
    ],
):
    return await classroom_service.get_classroom_by_id_with_students(
        classroom_id=classroom_id,
        teacher_id=teacher.id,
    )


@router.post("/create_classroom")
async def create_classroom(
    classroom_create: ClassroomCreate,
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    classroom_service: Annotated[
        "ClassroomsService",
        Depends(get_service(ClassroomsService)),
    ],
):
    return await classroom_service.create_classroom(
        classroom_create=classroom_create,
        teacher_id=teacher.id,
    )


@router.post("/add_student_to_classroom")
async def add_student_to_classroom(
    classroom_id: UUID,
    student_id: UUID,
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    classroom_service: Annotated[
        "ClassroomsService",
        Depends(get_service(ClassroomsService)),
    ],
):
    return await classroom_service.add_student_to_classroom(
        classroom_id=classroom_id,
        teacher_id=teacher.id,
        student_id=student_id,
    )
