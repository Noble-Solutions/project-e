import aioboto3

from types_aiobotocore_s3 import S3Client
from config import settings


class AIOBoto3Client:
    """Singleton class to manage aioboto3 session and client."""

    @staticmethod
    async def get_client() -> S3Client:
        async with aioboto3.Session().client(
            service_name="s3",
            endpoint_url="https://storage.yandexcloud.net",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        ) as client:
            yield client


boto_client_helper = AIOBoto3Client()
