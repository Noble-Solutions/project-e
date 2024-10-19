from typing import Annotated, Optional

from fastapi import APIRouter, Depends

from core.exceptions import invalid_data_for_register_exc
from core.schemas.user import AccessTokenPayload
from core.services.get_service import get_service
from core.services.variants import VariantsService
from core.utils.auth_utils import get_current_user

router = APIRouter(
    prefix="/variants",
    tags=["variants"],
)


#
@router.get("/get_all_variants_of_student")
async def get_all_variants_of_student(
    user: Annotated[
        "AccessTokenPayload",
        Depends(get_current_user),
    ],
    variants_service: Annotated[
        "VariantsService",
        Depends(get_service(VariantsService)),
    ],
    student_id: Optional[int] = None,
):
    """
    Retrieves all variants associated with a specific student.

    Parameters:
        user (Annotated[AccessTokenPayload]): The user making the request.
        variants_service (Annotated[VariantsService]): The variants service dependency.
        student_id (Optional[int]): The ID of the student, if the user is a teacher.

    Raises:
        invalid_data_for_register_exc: If the user is neither a teacher nor a student, or if the user is a student
        but student ID is provided.

    Returns:
        A list of all variants associated with the student.
    """
    if user.role_type == "teacher" and student_id:
        id_to_use = student_id
    elif user.role_type == "student" and not student_id:
        id_to_use = user.id
    else:
        raise invalid_data_for_register_exc
    return await variants_service.get_all_variants_of_student(id_to_use)
