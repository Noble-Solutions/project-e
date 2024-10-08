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
    if user.role_type == "teacher" and student_id:
        id_to_use = student_id
    elif user.role_type == "student" and not student_id:
        id_to_use = user.id
    else:
        raise invalid_data_for_register_exc
    return await variants_service.get_all_variants_of_student(id_to_use)
