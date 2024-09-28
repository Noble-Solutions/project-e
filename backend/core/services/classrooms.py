from typing import List, Dict
from uuid import UUID

from sqlalchemy import select

from core.models import Classroom, Student
from core.schemas import ClassroomCreate, ClassroomRead
from .base_service import BaseService


class ClassroomsService(BaseService):
    async def get_all_classrooms_of_teacher(
        self,
        teacher_id: UUID,
    ) -> Dict[str, List[ClassroomRead]]:
        stmt = select(Classroom).where(Classroom.teacher_id == teacher_id)
        classrooms = await self.db.scalars(stmt)
        return {
            "classrooms": [
                ClassroomRead.model_validate(classroom) for classroom in classrooms
            ]
        }

    async def create_classroom(
        self,
        classroom_create: ClassroomCreate,
        teacher_id: UUID,
    ):
        classroom = Classroom(
            **classroom_create.model_dump(),
            amount_of_students=0,
            teacher_id=teacher_id,
        )
        self.db.add(classroom)
        await self.db.commit()

    async def add_student_to_classroom(self, classroom_id: UUID, student_id: UUID):
        stmt = select(Classroom).where(Classroom.id == classroom_id)
        stmt2 = select(Student).where(Student.id == student_id)
        classroom = await self.db.scalar(stmt)
        student = await self.db.scalar(stmt2)
        classroom.students.append(student)
        classroom.amount_of_students += 1
        await self.db.commit()

    async def remove_student_from_classroom(self, classroom_id: int, student_id: int):
        stmt = select(Classroom).where(Classroom.id == classroom_id)
        classroom = await self.db.scalar(stmt)
        classroom.students.remove(student_id)
        await self.db.commit()
