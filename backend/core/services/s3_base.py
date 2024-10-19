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
        """
        Asynchronously generates a presigned URL for uploading a file to an S3 bucket.

        Args:
            full_file_name (str): The full name of the file including the path.

        Returns:
            dict: A dictionary containing the presigned URL and other necessary information for uploading the file.

        Raises:
            HTTPException: If there is an error generating the presigned URL.
        """
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
        """
        Asynchronously generates a presigned URL for downloading a file from an S3 bucket.

        Args:
            full_file_name (str): The full name of the file including file name and extension.

        Returns:
            str: The presigned URL for downloading the file.

        Raises:
            HTTPException: If there is an error generating the presigned URL.
        """
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
