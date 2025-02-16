import random
from http import HTTPStatus

import aiohttp
import pytest
import pytest_asyncio
from .utils import get_all_tasks_of_teacher
from .utils import get_all_classrooms_of_user

pytestmark = pytest.mark.asyncio

student_id = "ea6d93ec-5834-4b12-8dfa-ecac87cd1059"


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {
                "username": f"userlogin{random.randint(1000, 9999)}",
                "password": "userpassword",
                "first_name": "userfirstname",
                "last_name": "userpass",
                "role_type": "teacher",
                "subject": "math",
            },
            {"status": HTTPStatus.CREATED.value},
        ),
    ],
)
@pytest.mark.asyncio
async def test_signup(query_data, expected_answer):
    session = aiohttp.ClientSession()
    url = "http://localhost:8000/api/auth/register"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    async with session.post(url, headers=headers, json=query_data) as response:
        print(query_data)
        status = response.status
        print(response)
    await session.close()
    assert status == expected_answer.get("status")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"username": "string", "password": "string"},
            {"status": HTTPStatus.OK.value},
        ),
    ],
)
@pytest.mark.asyncio
async def test_login(query_data, expected_answer):
    session = aiohttp.ClientSession()
    url = "http://localhost:8000/api/auth/login"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    async with session.post(url, headers=headers, data=query_data) as response:
        status = response.status
    await session.close()
    assert status == expected_answer.get("status")


# test wrong login
@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"username": "wronglogintest1234", "password": "string"},
            {"status": HTTPStatus.UNAUTHORIZED.value},
        ),
    ],
)
@pytest.mark.asyncio
async def test_wrong_login(query_data, expected_answer):
    session = aiohttp.ClientSession()
    url = "http://localhost:8000/api/auth/login"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    async with session.post(url, headers=headers, data=query_data) as response:
        status = response.status
    await session.close()
    assert status == expected_answer.get("status")


@pytest_asyncio.fixture(scope="session")
async def access_token():
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8000/api/auth/login",
            data={
                "username": "string",
                "password": "string",
            },
        ) as response:
            login_data = await response.json()
            if response.status == 200:
                access_token = login_data.get("access_token")
                return access_token
            else:
                pytest.fail(
                    f"Failed to get access token: {response.status} with {login_data}"
                )


@pytest_asyncio.fixture(scope="session")
async def student_access_token():
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8000/api/auth/login",
            data={
                "username": "zyxolol",
                "password": "123",
            },
        ) as response:
            login_data = await response.json()
            if response.status == 200:
                student_access_token = login_data.get("access_token")
                return student_access_token
            else:
                pytest.fail(
                    f"Failed to get access token: {response.status} with {login_data}"
                )


@pytest_asyncio.fixture(scope="session")
async def test_create_classroom(access_token):
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/api/classrooms/create_classroom"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        async with session.post(
            url,
            headers=headers,
            json={
                "name": "11 Е",
            },
        ) as response:
            response_json = await response.json()
            if response.status != 201:
                pytest.fail(
                    f"Failed to create classroom: {response.status} with {response_json}"
                )

            return response_json.get("id")


@pytest.mark.asyncio
async def test_add_student(access_token, test_create_classroom):
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/api/classrooms/add_student"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        async with session.post(
            url,
            headers=headers,
            params={
                "classroom_id": test_create_classroom,
                "student_id": student_id,
            },
        ) as response:
            response_json = await response.json()
            if response.status != 200:
                pytest.fail(
                    f"Failed to add student to classroom: {response.status} with {response_json}"
                )
            print(response_json)


@pytest.mark.asyncio
async def test_get_classroom_by_id_with_students(access_token, test_create_classroom):
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/api/classrooms/get_classroom_by_id_with_students"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        async with session.get(
            url,
            headers=headers,
            params={
                "classroom_id": test_create_classroom,
            },
        ) as response:
            response_json = await response.json()
            if response.status != 200:
                pytest.fail(
                    f"Failed to get classroom: {response.status} with {response_json}"
                )
            assert "classroom" in response_json.keys()
            assert "students" in response_json.get("classroom").keys()
            assert "classroom_data" in response_json.get("classroom").keys()
            assert (
                response_json.get("classroom").get("classroom_data").get("name")
                == "11 Е"
            )
            assert (
                "amount_of_students"
                in response_json.get("classroom").get("classroom_data").keys()
            )


@pytest.mark.asyncio
async def test_get_all_classrooms_of_user(access_token):
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/api/classrooms/get_all_classrooms_of_user"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        async with session.get(
            url,
            headers=headers,
        ) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to get classrooms: {response.status} with {response_json}"
                )
            assert "classrooms" in response_json.keys()


async def test_update_classroom(access_token, test_create_classroom):
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/api/classrooms/update_classroom"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        async with session.put(
            url,
            headers=headers,
            params={
                "classroom_id": test_create_classroom,
            },
            json={
                "name": "Новое имя",
            },
        ) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to update classroom: {response.status} with {response_json}"
                )
        classroom = await get_all_classrooms_of_user(headers)
        print(classroom)
        assert classroom[0].get("classroom_data")["name"] == "Новое имя"
        assert classroom[0].get("classroom_data")["id"] == test_create_classroom
        assert classroom[0].get("classroom_data")["subject"] == "informatics"


@pytest.mark.asyncio
async def test_remove_student(access_token, test_create_classroom):
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/api/classrooms/delete_student"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        async with session.delete(
            url,
            headers=headers,
            params={
                "classroom_id": test_create_classroom,
                "student_id": student_id,
            },
        ) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to remove student from classroom: {response.status} with {response_json}"
                )
            # print(response_json)


@pytest.mark.asyncio
async def test_delete_classroom(access_token, test_create_classroom):
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/api/classrooms/delete_classroom"
        url_to_check_classrooms = (
            "http://localhost:8000/api/classrooms/get_all_classrooms_of_user"
        )
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        async with session.delete(
            url,
            headers=headers,
            params={
                "classroom_id": test_create_classroom,
            },
        ) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to delete classroom: {response.status} with {response_json}"
                )
            print(response_json)


@pytest_asyncio.fixture(scope="session")
async def test_create_task(access_token):
    async with aiohttp.ClientSession() as session:

        url = "http://localhost:8000/api/tasks/create_task"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        payload = {
            "task_create": {
                "text": "reshite kakoi-to tekst",
                "type": 13,
                "type_of_answer": "short_answer",
                "correct_answer": "2354",
            }
        }
        async with session.post(url, headers=headers, json=payload) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 201:
                pytest.fail(
                    f"Failed to create task: {response.status} with {response_json}"
                )
            if "id" not in response_json.keys():
                pytest.fail(f"Field id not found in response: {response_json}")
            return response_json.get("id")


@pytest.mark.asyncio
async def test_get_all_tasks_of_teacher(access_token, test_create_task):
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/api/tasks/get_all_tasks_of_teacher"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        async with session.get(url, headers=headers) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to get tasks: {response.status} with {response_json}"
                )
            if tasks := response_json.get("tasks"):
                if isinstance(tasks, list):
                    assert len(tasks) == 1
                    assert tasks[0].get("id") == test_create_task
                else:
                    pytest.fail(f"Tasks field is not a list: {tasks}")
            else:
                pytest.fail(f"Field tasks not found in response: {response_json}")


@pytest.mark.asyncio
async def test_update_task(access_token, test_create_task):
    async with aiohttp.ClientSession() as session:
        url = f"http://localhost:8000/api/tasks/{test_create_task}/"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        payload = {
            "task_id": test_create_task,
            "task_update": {
                "text": "ne reshite kakoi-to tekst",
                "type": 12,
                "type_of_answer": "full_answer",
            },
        }
        async with session.put(url, headers=headers, json=payload) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to update task: {response.status} with {response_json}"
                )

        tasks = await get_all_tasks_of_teacher(headers)
        assert len(tasks) == 1
        print(tasks[0])
        assert tasks[0].get("text") == "ne reshite kakoi-to tekst"
        assert tasks[0].get("type") == 12
        assert tasks[0].get("type_of_answer") == "full_answer"
        assert tasks[0].get("correct_answer") is None
        assert tasks[0].get("id") == test_create_task


@pytest.mark.asyncio
async def test_delete_task(access_token, test_create_task):
    async with aiohttp.ClientSession() as session:
        url = f"http://localhost:8000/api/tasks/{test_create_task}/"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        async with session.delete(
            url,
            headers=headers,
        ) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to delete task: {response.status} with {response_json}"
                )
        tasks = await get_all_tasks_of_teacher(headers)
        assert len(tasks) == 0


@pytest_asyncio.fixture(scope="session")
async def test_create_variant(access_token):
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/api/variants/"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        async with session.post(
            url,
            headers=headers,
            json={
                "name": "Вариант 15.01.2025",
            },
        ) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 201:
                pytest.fail(
                    f"Failed to create variant: {response.status} with {response_json}"
                )
            if "id" not in response_json.keys():
                pytest.fail(f"Field id not found in response: {response_json}")
            print(response_json)
            return response_json.get("id")


@pytest.mark.asyncio
async def test_add_task_to_variant(access_token, test_create_variant):
    async with aiohttp.ClientSession() as session:
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # Creating task to add in the variant
        url = "http://localhost:8000/api/tasks/create_task"
        payload = {
            "task_create": {
                "text": "reshite kakoi-to tekst",
                "type": 14,
                "type_of_answer": "short_answer",
                "correct_answer": "1337",
            }
        }
        async with session.post(url, headers=headers, json=payload) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 201:
                pytest.fail(
                    f"Failed to create task: {response.status} with {response_json}"
                )
            if "id" not in response_json.keys():
                pytest.fail(f"Field id not found in response: {response_json}")
            task_id = response_json.get("id")

        url = f"http://localhost:8000/api/variants/add_task/{test_create_variant}/task/{task_id}"
        async with session.post(
            url,
            headers=headers,
        ) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()

            if response.status != 200:
                pytest.fail(
                    f"Failed to add task to variant: {response.status} with {response_json}"
                )


@pytest.mark.asyncio
async def test_get_all_variants_of_teacher(access_token, test_create_variant):
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/api/variants/"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        async with session.get(url, headers=headers) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to get all variants: {response.status} with {response_json}"
                )
            assert len(response_json.get("variants")) == 1
            assert (
                response_json.get("variants")[0].get("variant_data").get("name")
                == "Вариант 15.01.2025"
            )
            assert (
                response_json.get("variants")[0].get("variant_data").get("id")
                == test_create_variant
            )


@pytest.mark.asyncio
async def test_get_variant_by_id_with_tasks(access_token, test_create_variant):
    async with aiohttp.ClientSession() as session:
        url = f"http://localhost:8000/api/variants/{test_create_variant}/"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        async with session.get(url, headers=headers) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to get variant: {response.status} with {response_json}"
                )
            print(f"get_variant_by_id_with_tasks response_json: {response_json}")
            assert len(response_json.get("variant").get("tasks")) == 1
            assert (
                response_json.get("variant").get("tasks")[0].get("text")
                == "reshite kakoi-to tekst"
            )
            assert (
                response_json.get("variant").get("variant_data").get("id")
                == test_create_variant
            )
            assert (
                response_json.get("variant")
                .get("variant_data")
                .get("maximum_score_from_short_answer_task")
                == 1
            )


@pytest.mark.asyncio
async def test_update_variant(access_token, test_create_variant):
    async with aiohttp.ClientSession() as session:
        url = f"http://localhost:8000/api/variants/{test_create_variant}/"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        payload = {
            "name": "Новое имя варианта",
        }
        async with session.put(url, headers=headers, json=payload) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to update variant: {response.status} with {response_json}"
                )

        async with session.get(url, headers=headers) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to get variant: {response.status} with {response_json}"
                )
            assert len(response_json.get("variant").get("tasks")) == 1
            assert (
                response_json.get("variant").get("tasks")[0].get("text")
                == "reshite kakoi-to tekst"
            )
            assert (
                response_json.get("variant").get("variant_data").get("id")
                == test_create_variant
            )
            assert (
                response_json.get("variant").get("variant_data").get("name")
                == "Новое имя варианта"
            )


@pytest.mark.asyncio
async def test_check_variant(access_token, test_create_variant):
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/api/tasks/create_task"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        payload = {
            "task_create": {
                "text": "reshite kakoi-to tekst",
                "type": 13,
                "type_of_answer": "short_answer",
                "correct_answer": "2354",
            }
        }
        async with session.post(url, headers=headers, json=payload) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 201:
                pytest.fail(
                    f"Failed to create task: {response.status} with {response_json}"
                )
            if "id" not in response_json.keys():
                pytest.fail(f"Field id not found in response: {response_json}")

            task_id = response_json.get("id")

        # ------------------

        url = f"http://localhost:8000/api/variants/add_task/{test_create_variant}/task/{task_id}"
        async with session.post(
            url,
            headers=headers,
        ) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()

            if response.status != 200:
                pytest.fail(
                    f"Failed to add task to variant: {response.status} with {response_json}"
                )

        # ------------------

        url = f"http://localhost:8000/api/variants/{test_create_variant}/"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        async with session.get(url, headers=headers) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to get variant: {response.status} with {response_json}"
                )
            print(f"check_variant {response_json}")
        payload_full_correct = {
            task["id"]: task["correct_answer"]
            for task in response_json.get("variant").get("tasks")
        }
        payload_half_correct = {}

        for task in response_json.get("variant").get("tasks"):
            if task["correct_answer"] == "2354":
                payload_half_correct[task["id"]] = "123"
            else:
                payload_half_correct[task["id"]] = task["correct_answer"]

        url = f"http://localhost:8000/api/variants/check/{test_create_variant}"
        print(payload_full_correct)
        print(payload_half_correct)
        async with session.get(
            url, headers=headers, json=payload_full_correct
        ) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to check variant: {response.status} with {response_json}"
                )
            assert response_json.get("points_earned_by_student") == 2
            assert response_json.get("maximum_points") == 2

        async with session.get(
            url, headers=headers, json=payload_half_correct
        ) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to check variant: {response.status} with {response_json}"
                )
            assert response_json.get("points_earned_by_student") == 1
            assert response_json.get("maximum_points") == 2


@pytest.mark.asyncio
async def test_assign_variant_to_student(
    access_token,
    student_access_token,
    test_create_variant,
):
    url = f"http://localhost:8000/api/variants/assign_to_student/{test_create_variant}/{student_id}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            print(response_json)
            if response.status != 200:
                pytest.fail(
                    f"Failed to assign variant to student: {response.status} with {response_json}"
                )
    headers["Authorization"] = f"Bearer {student_access_token}"
    url = "http://localhost:8000/api/variants"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            print(response_json)
            if response.status != 200:
                pytest.fail(
                    f"Failed to assign variant to student: {response.status} with {response_json}"
                )
            assert (
                response_json.get("variants")[0].get("variant_data").get("id")
                == test_create_variant
            )


@pytest.mark.asyncio
async def test_remove_task_from_variant(access_token, test_create_variant):
    async with aiohttp.ClientSession() as session:
        url = f"http://localhost:8000/api/variants/{test_create_variant}/"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        async with session.get(url, headers=headers) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to get variant: {response.status} with {response_json}"
                )

        task_id = response_json.get("variant").get("tasks")[0].get("id")
        url = f"http://localhost:8000/api/variants/remove_task/{test_create_variant}/task/{task_id}"
        async with session.delete(url, headers=headers) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to delete task from variant: {response.status} with {response_json}"
                )


@pytest.mark.asyncio
async def test_delete_data(access_token):
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/api/delete_test_data"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        async with session.post(url, headers=headers) as response:
            try:
                response_json = await response.json()
            except aiohttp.ContentTypeError:
                response_json = await response.text()
            if response.status != 200:
                pytest.fail(
                    f"Failed to delete test data: {response.status} with {response_json}"
                )
            print(response_json)
