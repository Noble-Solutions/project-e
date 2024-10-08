from typing import List, Dict
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from core.models import Classroom, Student, StudentClassroomAssociation
from core.schemas import ClassroomCreate, ClassroomRead
from .base_service import BaseService
from ..exceptions import forbidden_exc, student_already_in_classroom_exc
from ..schemas.user import StudentRead, TeacherRead


class ClassroomsService(BaseService):
    async def get_all_classrooms_of_teacher(
        self,
        teacher_id: UUID,
    ):
        stmt = select(Classroom).where(Classroom.teacher_id == teacher_id)
        classrooms = await self.db.scalars(stmt)
        return {
            "classrooms": [
                {
                    "classroom_data": ClassroomRead.model_validate(classroom),
                }
                for classroom in classrooms
            ]
        }

    async def get_all_classrooms_of_student(
        self,
        student_id: UUID,
    ):
        stmt = (
            select(Student)
            .where(Student.id == student_id)
            .options(selectinload(Student.classrooms).joinedload(Classroom.teacher))
        )
        student = await self.db.scalar(stmt)
        return {
            "classrooms": [
                {
                    "classroom_data": ClassroomRead.model_validate(classroom),
                    "teacher": TeacherRead.model_validate(classroom.teacher),
                }
                for classroom in student.classrooms
            ]
        }

    async def get_classroom_by_id_with_students(
        self,
        classroom_id: UUID,
        teacher_id: UUID,
    ) -> Dict[str, Dict[str, list[StudentRead] | ClassroomRead]]:
        stmt = (
            select(Classroom)
            .where(Classroom.id == classroom_id)
            .options(selectinload(Classroom.students))
        )
        classroom = await self.db.scalar(stmt)
        if classroom.teacher_id != teacher_id:
            raise forbidden_exc
        return {
            "classroom_with_students": {
                "classroom": ClassroomRead.model_validate(classroom),
                "students": [
                    StudentRead.model_validate(student)
                    for student in classroom.students
                ],
            }
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

    async def add_student_to_classroom(
        self,
        classroom_id: UUID,
        student_id: UUID,
        teacher_id: UUID,
    ):
        stmt = (
            select(Classroom)
            .where(Classroom.id == classroom_id)
            .options(selectinload(Classroom.students))
        )
        classroom = await self.db.scalar(stmt)
        print(classroom)
        if classroom.teacher_id != teacher_id:
            raise forbidden_exc
        stmt2 = select(Student).where(Student.id == student_id)
        student = await self.db.scalar(stmt2)
        if student in classroom.students:
            raise student_already_in_classroom_exc
        classroom.students.append(student)
        classroom.amount_of_students += 1
        await self.db.commit()

    async def remove_student_from_classroom(
        self,
        classroom_id: UUID,
        student_id: UUID,
    ):
        stmt = select(Classroom).where(Classroom.id == classroom_id)
        classroom = await self.db.scalar(stmt)
        classroom.students.remove(student_id)
        await self.db.commit()
