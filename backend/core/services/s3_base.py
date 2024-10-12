from botocore.exceptions import ClientError
from fastapi import HTTPException
from types_aiobotocore_s3 import S3Client

from config import settings
from core.utils.s3_utils import generate_signed_url


class S3BaseService:
    def __init__(self, client: S3Client):
        self.client = client

    async def get_presigned_url_for_upload_to_s3(
        self,
        full_file_name: str,
    ):
        try:
            response = await self.client.generate_presigned_post(
                Bucket=settings.s3_bucket_name,
                Key=full_file_name,
                Conditions=None,
                ExpiresIn=3600,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return response

    async def get_presigned_url_for_get_from_s3(
        self,
        full_file_name: str,
    ):
        try:
            response = await self.client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": settings.s3_bucket_name,
                    "Key": full_file_name,
                },
                ExpiresIn=3600,
            )
        except ClientError as e:
            raise HTTPException(status_code=500, detail=str(e))

        return response
