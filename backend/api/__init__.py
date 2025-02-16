from fastapi import APIRouter
from .auth import router as auth_router
from .tests import router as tests_router

from .variants import router as variants_router
from .classrooms import router as classrooms_router

from .tasks import router as tasks_router

router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(tests_router)
router.include_router(variants_router)
router.include_router(classrooms_router)
router.include_router(tasks_router)
