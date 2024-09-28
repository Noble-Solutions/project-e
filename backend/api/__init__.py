from fastapi import APIRouter
from .auth import router as auth_router
from .variants import router as variants_router
from .classrooms import router as classrooms_router

router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(variants_router)
router.include_router(classrooms_router)
