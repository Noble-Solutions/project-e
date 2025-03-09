from uuid import UUID

from sqlalchemy import select

from core.models import StudentPerformance
from core.schemas.analytics import TaskStatCreate, TaskStatRead
from core.services.base_service import BaseService


class AnalyticsService(BaseService):
    async def add_task_result(
        self,
        task_stat_create: TaskStatCreate,
    ):
        stmt = select(StudentPerformance).where(
            StudentPerformance.classroom_id == task_stat_create.classroom_id,
            StudentPerformance.student_id == task_stat_create.student_id,
            StudentPerformance.task_type == task_stat_create.task_type,
        )
        task_stat_row = await self.db.scalar(stmt)
        if task_stat_row is None:
            task_stat_row = StudentPerformance(**task_stat_create.model_dump())
            self.db.add(task_stat_row)
        else:
            task_stat_row.correct_solved += task_stat_create.correct_solved
            task_stat_row.total_solved += task_stat_create.total_solved
        await self.db.commit()

    async def get_performance_of_student_in_classroom(
        self,
        student_id: UUID,
        classroom_id: UUID,
    ):
        stmt = select(StudentPerformance).where(
            StudentPerformance.student_id == student_id,
            StudentPerformance.classroom_id == classroom_id,
        )
        task_stats = await self.db.scalars(stmt)
        return {
            "task_stats": [
                {
                    "task_stat": TaskStatRead.model_validate(task),
                }
                for task in task_stats
            ]
        }
