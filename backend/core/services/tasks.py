from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import select

from core.schemas.tasks import TaskCreate, TaskRead
from core.services.base_service import BaseService
from .s3_base import S3BaseService
from ..models import Task
from .get_service import get_s3_service


class TasksService(BaseService):
    async def get_all_tasks_of_teacher(self, teacher_id: UUID):
        """
        Asynchronously retrieves all tasks associated with a teacher.

        Args:
            teacher_id (UUID): The ID of the teacher.

        Returns:
            List[TaskRead]: A list of TaskRead objects representing the tasks associated with the teacher.
        """
        stmt = select(Task).where(Task.teacher_id == teacher_id)
        tasks = await self.db.scalars(stmt)
        return [TaskRead.model_validate(task) for task in tasks]

    async def create_task(
        self,
        task_create: TaskCreate,
        teacher_id: UUID,
        file_extension: Optional[str],
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
        self.db.add(task)
        await self.db.commit()
        return TaskRead.model_validate(task)
