# from botocore.client import BaseClient
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from types_aiobotocore_s3 import S3Client

from config import settings
from core.botoclient_helper import boto_client_helper
from core.services.get_service import get_s3_service
from core.services.s3_base import S3BaseService

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
