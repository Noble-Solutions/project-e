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
        """
        Asynchronously retrieves all classrooms associated with a teacher.

        Args:
            teacher_id (UUID): The ID of the teacher.

        Returns:
            dict: A dictionary containing a list of classrooms, where each classroom is represented by a dictionary with the key "classroom_data" and the value being the result of calling `ClassroomRead.model_validate(classroom)`.
        """
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
        """
        Asynchronously retrieves all classrooms associated with a student.

        Args:
            student_id (UUID): The ID of the student.

        Returns:
            dict: A dictionary containing a list of classrooms, where each classroom is represented by a dictionary with the keys "classroom_data" and "teacher". The "classroom_data" value is the result of calling `ClassroomRead.model_validate(classroom)`, and the "teacher" value is the result of calling `TeacherRead.model_validate(classroom.teacher)`.
        """
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
        """
        Asynchronously retrieves a classroom by its ID along with its associated students.

        Args:
            classroom_id (UUID): The ID of the classroom to retrieve.
            teacher_id (UUID): The ID of the teacher associated with the classroom.

        Returns:
            dict: A dictionary containing a dictionary with the keys "classroom_with_students" and "students".
                  The "classroom_with_students" value is a dictionary with the keys "classroom" and "students".
                  The "classroom" value is the result of calling `ClassroomRead.model_validate(classroom)`
                  and the "students" value is a list of dictionaries, where each dictionary is the result of
                  calling `StudentRead.model_validate(student)` for each student in the
                  "classroom.students" list.
        """
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
        """
        Asynchronously creates a new classroom.

        Args:
            classroom_create (ClassroomCreate): The data for creating the classroom.
            teacher_id (UUID): The ID of the teacher associated with the classroom.

        Returns:
            None
        """
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
        """
        Asynchronously adds a student to a classroom.

        Args:
            classroom_id (UUID): The ID of the classroom to add the student to.
            student_id (UUID): The ID of the student to add to the classroom.
            teacher_id (UUID): The ID of the teacher associated with the classroom.

        Raises:
            forbidden_exc: If the teacher ID does not match the teacher ID of the classroom.
            student_already_in_classroom_exc: If the student is already in the classroom.

        Returns:
            None
        """
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
        """
        Asynchronously removes a student from a classroom.

        Args:
            classroom_id (UUID): The ID of the classroom to remove the student from.
            student_id (UUID): The ID of the student to remove from the classroom.

        Raises:
            None.

        Returns:
            None.
        """
        stmt = select(Classroom).where(Classroom.id == classroom_id)
        classroom = await self.db.scalar(stmt)
        classroom.students.remove(student_id)
        await self.db.commit()
