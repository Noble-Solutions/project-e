import aiohttp

from core.schemas import ClassroomRead
from core.schemas.tasks import TaskRead


async def get_all_tasks_of_teacher(headers) -> list[TaskRead]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://localhost:8000/api/tasks/get_all_tasks_of_teacher",
            headers=headers,
        ) as response:
            response_json = await response.json()
            tasks = response_json.get("tasks")

    return tasks


async def get_all_classrooms_of_user(headers) -> list[ClassroomRead]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://localhost:8000/api/classrooms/get_all_classrooms_of_user",
            headers=headers,
        ) as response:
            response_json = await response.json()
            classrooms = response_json.get("classrooms")

    return classrooms
