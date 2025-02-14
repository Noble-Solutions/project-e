from uuid import UUID

from fastapi import APIRouter, Depends
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette import status

from core.models import Classroom, StudentClassroomAssociation
from core.schemas import ClassroomCreate
from core.schemas.user import AccessTokenPayload
from core.services.get_service import get_service
from core.utils.auth_utils import (
    get_current_teacher,
    get_current_student,
    get_current_user,
)
from core.services.classrooms import ClassroomsService

router = APIRouter(
    prefix="/classrooms",
    tags=["classrooms"],
)


@router.get("/get_all_classrooms_of_user", status_code=status.HTTP_200_OK)
async def get_all_classrooms_of_user(
    user: Annotated[
        "AccessTokenPayload",
        Depends(get_current_user),
    ],
    classroom_service: Annotated[
        "ClassroomsService",
        Depends(get_service(ClassroomsService)),
    ],
):
    """
    Retrieves all classrooms associated with the current user.

    Parameters:
        - user (Annotated[AccessTokenPayload]): The user making the request.
        - classroom_service (Annotated[ClassroomsService]): The classrooms service dependency.

    Returns:
        A list of all classrooms associated with the current user.
    """
    if user.role_type == "teacher":
        return await classroom_service.get_all_classrooms_of_teacher(
            teacher_id=user.id,
        )
    if user.role_type == "student":
        return await classroom_service.get_all_classrooms_of_student(
            student_id=user.id,
        )


@router.get("/get_classroom_by_id_with_students", status_code=status.HTTP_200_OK)
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
    """
    Retrieves a classroom by its ID along with its associated students.

    Parameters:
        - classroom_id (UUID): The ID of the classroom to retrieve.
        - teacher (Annotated[AccessTokenPayload]): The teacher making the request.
        - classroom_service (Annotated[ClassroomsService]): The classrooms service dependency.

    Returns:
        The classroom with its associated students.
    """
    return await classroom_service.get_classroom_by_id_with_students(
        classroom_id=classroom_id,
        teacher_id=teacher.id,
    )


@router.post("/create_classroom", status_code=status.HTTP_201_CREATED)
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
    """
    Creates a new classroom.

    Args:
        classroom_create (ClassroomCreate): The url_fields_dictionary for creating the classroom.
        teacher (Annotated[AccessTokenPayload]): The teacher making the request.
        classroom_service (Annotated[ClassroomsService]): The classrooms service dependency.

    Returns:
        The created classroom.
    """
    return await classroom_service.create_classroom(
        classroom_create=classroom_create,
        teacher_id=teacher.id,
    )


@router.put("/update_classroom", status_code=status.HTTP_200_OK)
async def update_classroom(
    classroom_id: UUID,
    classroom_update: ClassroomCreate,
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    classroom_service: Annotated[
        "ClassroomsService",
        Depends(get_service(ClassroomsService)),
    ],
):
    return await classroom_service.update_classroom(
        classroom_id=classroom_id,
        classroom_update=classroom_update,
        teacher_id=teacher.id,
    )


@router.delete("/delete_classroom", status_code=status.HTTP_200_OK)
async def delete_classroom(
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
    await classroom_service.delete_classroom(
        classroom_id=classroom_id,
        teacher_id=teacher.id,
    )


@router.get("/find_student", status_code=status.HTTP_200_OK)
async def find_student(
    student_name: str,
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    classroom_service: Annotated[
        "ClassroomsService",
        Depends(get_service(ClassroomsService)),
    ],
):
    return await classroom_service.find_student_by_username(
        username=student_name,
    )


@router.post("/add_student", status_code=status.HTTP_200_OK)
async def add_student(
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
    """
    Adds a student to a classroom.

    Args:
        classroom_id (UUID): The ID of the classroom to add the student to.
        student_id (UUID): The ID of the student to add to the classroom.
        teacher (Annotated["AccessTokenPayload"]): The teacher making the request.
        classroom_service (Annotated["ClassroomsService"]): The classrooms service dependency.

    Returns:
        The result of calling `classroom_service.add_student_to_classroom` with the provided arguments.
    """
    return await classroom_service.add_student_to_classroom(
        classroom_id=classroom_id,
        teacher_id=teacher.id,
        student_id=student_id,
    )


@router.delete("/delete_student", status_code=status.HTTP_200_OK)
async def delete_student(
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
    return await classroom_service.remove_student_from_classroom(
        classroom_id=classroom_id,
        student_id=student_id,
        teacher_id=teacher.id,
    )
