# from botocore.client import BaseClient
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Body, Path
from starlette import status
from types_aiobotocore_s3 import S3Client

from core.db.botoclient_helper import boto_client_helper
from core.schemas.tasks import TaskCreate, TaskRead, GetAllTasksResponseModel
from core.schemas.user import AccessTokenPayload
from core.services.get_service import get_s3_service, get_service
from core.services.s3_base import S3BaseService
from core.services.tasks import TasksService
from core.utils.auth_utils import get_current_teacher

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/check_boto_client_connection")
async def check_boto_client_connection(
    boto_client: Annotated[
        "S3Client",
        Depends(boto_client_helper.get_client),
    ],
):
    """
    Check the connection to the Boto client.

    This function uses the Boto client to list the available buckets. If the connection is successful,
    it returns a list of buckets. If there is an exception during the connection, it raises an HTTPException
    with a status code of 500 and the error message as the detail.

    Parameters:
        boto_client (Annotated[S3Client]): The Boto client dependency.

    Returns:
        List[Dict[str, Any]]: A list of buckets if the connection is successful.

    Raises:
        HTTPException: If there is an exception during the connection.
    """
    try:
        buckets = await boto_client.list_buckets()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return buckets


@router.get("/get_presigned_url_for_upload_to_s3")
async def get_presigned_url_for_upload_to_s3(
    full_file_name: str,
    s3_service=Depends(get_s3_service(service_class=S3BaseService)),
):
    """
    Asynchronously generates a presigned URL for uploading a file to an S3 bucket.

    Args:
        full_file_name (str): The full name of the file including the path.
        s3_service (S3BaseService, optional): The S3 service dependency. Defaults to the result of `get_s3_service` with `service_class=S3BaseService`.

    Returns:
        dict: A dictionary containing the presigned URL and other necessary information for uploading the file.

    Raises:
        HTTPException: If there is an error generating the presigned URL.
    """
    return await s3_service.get_presigned_url_for_upload_to_s3(full_file_name)


@router.get("/get_presigned_url_for_get_from_s3")
async def get_presigned_url_for_get_from_s3(
    full_file_name: str,
    s3_service=Depends(get_s3_service(service_class=S3BaseService)),
):
    """
    Asynchronously generates a presigned URL for downloading a file from an S3 bucket.

    Args:
        full_file_name (str): The full name of the file including file name and extension.
        s3_service (S3BaseService, optional): The S3 service dependency. Defaults to the result of `get_s3_service` with `service_class=S3BaseService`.

    Returns:
        str: The presigned URL for downloading the file.

    Raises:
        HTTPException: If there is an error generating the presigned URL.
    """
    response = await s3_service.get_presigned_url_for_get_from_s3(full_file_name)
    return response


@router.post("/create_task", status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    task_service: Annotated[
        "TasksService",
        Depends(get_service(TasksService)),
    ],
    s3_service: Annotated[
        "S3BaseService",
        Depends(get_s3_service(service_class=S3BaseService)),
    ],
    file_extension: Optional[str] = Body(default=None),
):
    task = await task_service.create_task(
        task_create=task_create,
        teacher_id=teacher.id,
        file_extension=file_extension,
    )
    print(task)
    if task.file_id:
        presigned_url_data_object = await s3_service.get_presigned_url_for_upload_to_s3(
            full_file_name=f"{task.file_id}.{file_extension}"
        )
        return {
            "task": task,
            "presigned_url_data_object": presigned_url_data_object,
        }

    return {"task": task}


@router.get(
    "/get_all_tasks_of_teacher",
    status_code=status.HTTP_200_OK,
    response_model=GetAllTasksResponseModel,
)
async def get_all_tasks_of_teacher(
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    task_service: Annotated[
        "TasksService",
        Depends(get_service(TasksService)),
    ],
):
    return await task_service.get_all_tasks_of_teacher(teacher_id=teacher.id)


@router.put(
    "/{task_id}/",
    status_code=status.HTTP_200_OK,
    response_model=TaskRead,
)
async def update_task(
    task_id: Annotated[UUID, Path],
    task_update: TaskCreate,
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    task_service: Annotated[
        "TasksService",
        Depends(get_service(TasksService)),
    ],
    s3_service: Annotated[
        "S3BaseService",
        Depends(get_s3_service(service_class=S3BaseService)),
    ],
    file_extension: Optional[str] = Body(default=None),
) -> TaskRead:
    return await task_service.update_task(
        task_id=task_id,
        task_update=task_update,
        teacher_id=teacher.id,
        file_extension=file_extension,
    )


@router.patch(
    "/{task_id}/",
    status_code=status.HTTP_200_OK,
    response_model=TaskRead,
)
async def update_task_partial(
    task_id: Annotated[UUID, Path],
    task_update: TaskCreate,
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    task_service: Annotated[
        "TasksService",
        Depends(get_service(TasksService)),
    ],
    s3_service: Annotated[
        "S3BaseService",
        Depends(get_s3_service(service_class=S3BaseService)),
    ],
    file_extension: Optional[str] = Body(default=None),
) -> TaskRead:
    return await task_service.update_task(
        task_id=task_id,
        task_update=task_update,
        teacher_id=teacher.id,
        file_extension=file_extension,
        partial=True,
    )


@router.delete(
    "/{task_id}/",
    status_code=status.HTTP_200_OK,
)
async def delete_task(
    task_id: Annotated[UUID, Path],
    teacher: Annotated[
        "AccessTokenPayload",
        Depends(get_current_teacher),
    ],
    task_service: Annotated[
        "TasksService",
        Depends(get_service(TasksService)),
    ],
):
    return await task_service.delete_task(task_id=task_id, teacher_id=teacher.id)
