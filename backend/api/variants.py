from fastapi import APIRouter

router = APIRouter(
    prefix="/variants",
    tags=["variants"],
)
#
# @router.get("/get_all_variants_of_student")
# async def get_all_variants_of_student():
