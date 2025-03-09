from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload, selectinload

from core.models import (
    Variant,
    VariantTaskAssociation,
    User,
    Task,
    StudentVariantAssociation,
    Classroom,
)
from core.models.base_user import RoleType
from core.models.task import AnswerType
from core.schemas.tasks import TaskRead
from core.schemas.user import UserRead
from core.schemas.variant import VariantRead, VariantCreate
from core.services.base_service import BaseService
from core.utils.exceptions import (
    forbidden_exc,
    task_already_in_variant_exc,
    student_already_in_classroom_exc,
)


class VariantsService(BaseService):
    async def get_all_variants_of_user(
        self,
        user_id: UUID,
        user_role: RoleType,
    ):
        """
        Asynchronously retrieves all variants associated with a teacher.

        Args:
            user_id (UUID): The ID of the user.
            user_role (RoleType): The role of the user.
        Returns:
            dict: A dictionary containing a list of variants, where each variant is represented by a dictionary with the key "variant_data" and the value being the result of calling `VariantRead.model_validate(variant)`.
        """
        print("in get all variants of user")
        print(user_role)
        if user_role == "teacher":
            stmt = select(Variant).where(Variant.teacher_id == user_id)
            variants = await self.db.scalars(stmt)
        if user_role == "student":
            print("in user role student")
            stmt = (
                select(User)
                .where(User.id == user_id)
                .options(selectinload(User.variants_of_student))
            )
            student = await self.db.scalar(stmt)
            variants = student.variants_of_student
            for variant in variants:
                print(VariantRead.model_validate(variant))
        return {
            "variants": [VariantRead.model_validate(variant) for variant in variants]
        }

    async def get_variant_by_id_with_tasks(
        self,
        variant_id: UUID,
        user_id: UUID,
        user_role: RoleType,
    ) -> dict[str, dict[str, list[TaskRead] | VariantRead]]:
        stmt = (
            select(Variant)
            .where(Variant.id == variant_id)
            .options(selectinload(Variant.tasks))
        )
        variant = await self.db.scalar(stmt)
        variant_data = VariantRead.model_dump(VariantRead.model_validate(variant))

        if user_role == "teacher":
            if variant.teacher_id != user_id:
                raise forbidden_exc

        if user_role == "student":
            stmt = (
                select(StudentVariantAssociation)
                .where(StudentVariantAssociation.student_id == user_id)
                .where(StudentVariantAssociation.variant_id == variant_id)
            )
            association = await self.db.scalar(stmt)
            if not association:
                raise forbidden_exc
            classroom_id = association.classroom_id
            print(f"classroom_id {classroom_id}")
            variant_data["classroom_id"] = classroom_id

        response = {
            "variant": {
                "variant_data": variant_data,
                "tasks": [TaskRead.model_validate(task) for task in variant.tasks],
            }
        }

        print(response)
        return response

    async def create_variant(
        self,
        variant_create: VariantCreate,
        teacher_id: UUID,
    ) -> VariantRead:
        """
        Asynchronously creates a new variant.

        Args:
            variant_create (VariantCreate): The data for creating the variant.
            teacher_id (UUID): The ID of the teacher associated with the variant.

        Returns:
            None
        """
        stmt = select(User).where(User.id == teacher_id)
        teacher = await self.db.scalar(stmt)
        if teacher.role_type != "teacher":
            raise forbidden_exc
        variant = Variant(
            **variant_create.model_dump(),
            subject=teacher.subject,
            maximum_score_from_short_answer_task=0,
            amount_of_tasks=0,
            teacher_id=teacher_id,
        )
        self.db.add(variant)
        await self.db.commit()
        return VariantRead.model_validate(variant)

    async def update_variant(
        self,
        variant_id: UUID,
        variant_update: VariantCreate,
        # VariantUpdate и VariantCreate это одно и то же
        teacher_id: UUID,
    ):
        stmt = select(Variant).where(
            Variant.id == variant_id,
        )
        variant = await self.db.scalar(stmt)
        if variant.teacher_id != teacher_id:
            raise forbidden_exc
        for name, value in variant_update.model_dump().items():
            setattr(variant, name, value)
        await self.db.commit()
        return VariantRead.model_validate(variant)

    async def delete_variant(
        self,
        teacher_id: UUID,
        variant_id,
    ):
        stmt = select(Variant).where(
            Variant.id == variant_id,
        )
        variant = await self.db.scalar(stmt)
        if variant.teacher_id != teacher_id:
            raise forbidden_exc
        await self.db.delete(variant)
        await self.db.commit()

    async def add_task_to_variant(
        self,
        variant_id: UUID,
        task_id: UUID,
        teacher_id: UUID,
    ):
        """
        Asynchronously adds a task to a variant.

        Args:
            variant_id (UUID): The ID of the variant to add the task to.
            task_id (UUID): The ID of the task to add to the variant.
            teacher_id (UUID): The ID of the teacher associated with the variant.

        Raises:
            forbidden_exc: If the teacher ID does not match the teacher ID of the variant.
            task_already_in_variant_exc: If the task is already in the variant.

        Returns:
            None
        """
        stmt = (
            select(Variant)
            .where(Variant.id == variant_id)
            .options(selectinload(Variant.tasks))
        )
        variant = await self.db.scalar(stmt)
        print(variant)
        if variant.teacher_id != teacher_id:
            raise forbidden_exc
        stmt2 = select(Task).where(Task.id == task_id)
        task = await self.db.scalar(stmt2)
        if task in variant.tasks:
            raise task_already_in_variant_exc
        variant.tasks.append(task)
        variant.amount_of_tasks += 1
        variant.maximum_score_from_short_answer_task += task.points_per_task
        await self.db.commit()

    async def remove_task_from_variant(
        self,
        variant_id: UUID,
        task_id: UUID,
        teacher_id: UUID,
    ):
        stmt = select(Variant).where(Variant.id == variant_id)
        variant = await self.db.scalar(stmt)
        task = await self.db.scalar(select(Task).where(Task.id == task_id))
        if variant.teacher_id != teacher_id:
            raise forbidden_exc
        stmt3 = delete(VariantTaskAssociation).where(
            VariantTaskAssociation.task_id == task_id,
            VariantTaskAssociation.variant_id == variant_id,
        )
        variant.amount_of_tasks -= 1
        variant.maximum_score_from_short_answer_task -= task.points_per_task
        await self.db.execute(stmt3)
        try:
            await self.db.commit()
        except Exception as e:
            # Log the exception
            print(f"Error committing changes: {e}")
            await self.db.rollback()  # Rollback in case of error
            raise

        return {"status": "ok"}

    async def check_variant(
        self,
        variant_id: UUID,
        task_id_to_answer: dict[UUID, str | int],
    ):
        print("in check variant")
        stmt = (
            select(Variant)
            .where(Variant.id == variant_id)
            .options(selectinload(Variant.tasks))
        )
        variant = await self.db.scalar(stmt)

        variant_with_tasks_dict = {
            "variant_data": VariantRead.model_validate(variant),
            "tasks": [TaskRead.model_validate(task) for task in variant.tasks],
        }

        amount_of_points_earned_by_student = 0
        maximum_score_from_short_answer_task = variant_with_tasks_dict.get(
            "variant_data"
        ).maximum_score_from_short_answer_task

        """
        task_stats_for_analyctics
        это словарь в котором ключ это тип задания, а значение это список где первый элемент списка это 
        количество правильно решенных заданий, а второй - общее количество решенных заданий
        """
        task_stats_for_analytics: dict[int, list[int]] = {}

        for id_of_task, answer_of_student in task_id_to_answer.items():
            for task in variant_with_tasks_dict.get("tasks"):
                if task.type_of_answer != AnswerType.SHORT_ANSWER:
                    # TODO: Add support for other types of answers
                    continue
                if id_of_task == task.id:
                    if task.type not in task_stats_for_analytics.keys():
                        task_stats_for_analytics[task.type] = [0, 0]

                    task_stats_for_analytics[task.type][1] += 1
                    if task.correct_answer == answer_of_student:
                        amount_of_points_earned_by_student += task.points_per_task
                        task_stats_for_analytics[task.type][0] += 1

        return {
            "maximum_points": maximum_score_from_short_answer_task,
            "points_earned_by_student": amount_of_points_earned_by_student,
            "task_stats_for_analytics": task_stats_for_analytics,
        }

    async def assign_variant_to_student(
        self,
        variant_id: UUID,
        student_id: UUID,
        classroom_id: UUID,
        teacher_id: UUID,
    ):
        # Fetch the variant
        stmt = (
            select(Variant)
            .where(Variant.id == variant_id)
            .options(selectinload(Variant.students))
        )
        variant = await self.db.scalar(stmt)

        # Validate the variant
        if variant.teacher_id != teacher_id:
            raise forbidden_exc

        # Fetch the student
        stmt2 = select(User).where(User.id == student_id)
        student = await self.db.scalar(stmt2)

        # Check if the student is already in the variant
        if student in variant.students:
            raise student_already_in_classroom_exc

        # Create the association object
        association = StudentVariantAssociation(
            student_id=student.id,
            variant_id=variant.id,
            classroom_id=classroom_id,
        )

        # Add the association object to the session
        self.db.add(association)

        # Commit the transaction
        await self.db.commit()

        # Print the updated list of students in the variant (optional)
        for student in variant.students:
            print(UserRead.model_validate(student))

    async def assign_variant_to_all_students_in_classroom(
        self,
        variant_id: UUID,
        classroom_id: UUID,
        teacher_id: UUID,
    ):
        stmt = (
            select(Classroom)
            .where(Classroom.id == classroom_id)
            .options(selectinload(Classroom.students))
        )
        classroom = await self.db.scalar(stmt)
        if classroom.teacher_id != teacher_id:
            raise forbidden_exc

        for student in classroom.students:
            await self.assign_variant_to_student(
                variant_id=variant_id,
                student_id=student.id,
                teacher_id=teacher_id,
                classroom_id=classroom_id,
            )
