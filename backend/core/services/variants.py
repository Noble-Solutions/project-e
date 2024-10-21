from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from core.models import Variant, Student
from core.services.base_service import BaseService


class VariantsService(BaseService):
    async def get_all_variants_of_student(self, student_id: UUID):
        """
        Retrieves all variants associated with a specific student.

        Args:
            student_id (UUID): The ID of the student.

        Returns:
            List[Variant]: A list of variants associated with the student.
        """
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
