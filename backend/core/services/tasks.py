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
        stmt = select(Task).where(Task.teacher_id == teacher_id)
        tasks = await self.db.scalars(stmt)
        return [TaskRead.model_validate(task) for task in tasks]

    async def create_task(
        self,
        task_create: TaskCreate,
        teacher_id: UUID,
        file_extension: Optional[str],
    ) -> TaskRead:
        task = Task(
            **task_create.model_dump(),
            teacher_id=teacher_id,
        )
        if file_extension:
            task.file_id = uuid4()
        self.db.add(task)
        await self.db.commit()
        return TaskRead.model_validate(task)
