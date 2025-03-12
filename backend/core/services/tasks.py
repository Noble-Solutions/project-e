from typing import Optional, Dict, List
from uuid import UUID, uuid4

from sqlalchemy import select

from core.schemas.tasks import TaskCreate, TaskRead
from core.services.base_service import BaseService
from .s3_base import S3BaseService
from ..models import Task
from .get_service import get_s3_service
from ..utils.exceptions import forbidden_exc


class TasksService(BaseService):
    async def get_all_tasks_of_teacher(
        self, teacher_id: UUID
    ) -> dict[str, list[TaskRead]]:
        """
        Asynchronously retrieves all tasks associated with a teacher.

        Args:
            teacher_id (UUID): The ID of the teacher.

        Returns:
            List[TaskRead]: A list of TaskRead objects representing the tasks associated with the teacher.
        """
        stmt = select(Task).where(Task.teacher_id == teacher_id)
        tasks = await self.db.scalars(stmt)
        return {"tasks": [TaskRead.model_validate(task) for task in tasks]}

    async def create_task(
        self,
        task_create: TaskCreate,
        teacher_id: UUID,
        file_extension: Optional[str],
        additional_file_extension: Optional[str],
    ) -> TaskRead:
        """
        Asynchronously creates a new task in the database.

        Args:
            task_create (TaskCreate): An instance of the TaskCreate model containing the data for the new task.
            teacher_id (UUID): The ID of the teacher associated with the new task.
            file_extension (Optional[str]): The file extension of the task file, if applicable.

        Returns:
            TaskRead: An instance of the TaskRead model representing the newly created task.

        This function creates a new task in the database by creating a new Task instance with the data from the
        TaskCreate model and the provided teacher ID. If a file extension is provided, the task's file extension and
        file ID are set accordingly. The new task is then added to the database and committed. Finally, the newly
        created task is validated and returned as a TaskRead instance.
        """
        task = Task(
            **task_create.model_dump(),
            teacher_id=teacher_id,
        )
        if file_extension:
            task.file_extension = file_extension
            task.file_id = uuid4()
        if additional_file_extension:
            task.additional_file_extension = additional_file_extension
            task.additional_file_id = uuid4()
        self.db.add(task)
        await self.db.commit()
        return TaskRead.model_validate(task)

    async def update_task(
        self,
        task_id: UUID,
        task_update: TaskCreate,
        teacher_id: UUID,
        file_extension: Optional[str],
        partial: bool = False,
    ) -> TaskRead:
        """
        Asynchronously updates a task in the database.

        Args:
            task_id (UUID): The ID of the task to update.
            task_update (TaskCreate): An instance of the TaskCreate model containing the data for the updated task.
            teacher_id (UUID): The ID of the teacher associated with the updated task.
            file_extension (Optional[str]): The file extension of the updated task file, if applicable.

        Returns:
            TaskRead: An instance of the TaskRead model representing the updated task.

        This function retrieves the task with the given ID from the database, updates its data with the data
        """
        stmt = select(Task).where(Task.id == task_id)
        task = await self.db.scalar(stmt)
        if task.teacher_id != teacher_id:
            raise forbidden_exc
        for name, value in task_update.model_dump(exclude_unset=partial).items():
            setattr(task, name, value)
        await self.db.commit()
        return TaskRead.model_validate(task)

    async def delete_task(
        self,
        task_id: UUID,
        teacher_id: UUID,
    ) -> dict[str, bool]:
        """
        Asynchronously deletes a task from the database.

        Args:
            task_id (UUID): The ID of the task to delete.
            teacher_id (UUID): The ID of the teacher associated with the deleted task.

        Returns:
            TaskRead: An instance of the TaskRead model representing the deleted task.

        This function retrieves the task with the given ID from the database, deletes it from the database, and
        returns the deleted task.
        """
        stmt = select(Task).where(Task.id == task_id)
        task = await self.db.scalar(stmt)
        if task.teacher_id != teacher_id:
            raise forbidden_exc
        await self.db.delete(task)
        await self.db.commit()
        return {"ok": True}
