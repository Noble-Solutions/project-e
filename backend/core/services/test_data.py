from sqlalchemy import delete

from core.models import Classroom, Task, Variant
from core.services.base_service import BaseService


class TestDataService(BaseService):
    """
    Класс чтобы создавать и удалять  данные для тестов
    """

    async def create_test_data(self):
        # create mock classroom
        classroom = Classroom(
            name="test_classroom",
            subject="math",
            amount_of_students=0,
            teacher_id="45ae5b32-7c2b-46af-a451-00ad126fb80d",
        )
        self.db.add(classroom)
        await self.db.commit()

    async def delete_test_data(self):
        stmt = delete(Classroom).where(
            Classroom.teacher_id == "45ae5b32-7c2b-46af-a451-00ad126fb80d"
        )
        await self.db.execute(stmt)
        stmt = delete(Task).where(
            Task.teacher_id == "45ae5b32-7c2b-46af-a451-00ad126fb80d"
        )
        await self.db.execute(stmt)
        stmt = delete(Variant).where(
            Variant.teacher_id == "45ae5b32-7c2b-46af-a451-00ad126fb80d"
        )
        await self.db.execute(stmt)
        await self.db.commit()
        return {"status": "ok"}
