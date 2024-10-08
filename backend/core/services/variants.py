from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from core.models import Variant, Student
from core.services.base_service import BaseService


class VariantsService(BaseService):
    async def get_all_variants_of_student(self, student_id: int):
        stmt = (
            select(Variant)
            .options(
                selectinload(Variant.students),
                joinedload(Variant.teacher),
            )
            .where(Student.id == student_id)
        )
        variants = await self.db.scalars(stmt)
        return variants
