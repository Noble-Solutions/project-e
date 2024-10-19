# from botocore.client import BaseClient
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Body
from types_aiobotocore_s3 import S3Client

from config import settings
from core.botoclient_helper import boto_client_helper
from core.schemas.tasks import TaskCreate
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
    return await s3_service.get_presigned_url_for_upload_to_s3(full_file_name)


@router.get("/get_presigned_url_for_get_from_s3")
async def get_presigned_url_for_get_from_s3(
    full_file_name: str,
    s3_service=Depends(get_s3_service(service_class=S3BaseService)),
):
    response = await s3_service.get_presigned_url_for_get_from_s3(full_file_name)
    return response


@router.post("/create_task")
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
    file_extension: Optional[str] = Body(...),
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

    return {
        "task": task,
    }


@router.get("/get_all_tasks_of_teacher")
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
