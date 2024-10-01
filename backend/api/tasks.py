# from botocore.client import BaseClient
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from types_aiobotocore_s3 import S3Client

from core.botoclient_helper import boto_client_helper


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("check_boto_client_connection")
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
