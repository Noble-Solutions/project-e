import aioboto3
from contextlib import asynccontextmanager
from types_aiobotocore_s3 import S3Client
from config import settings


class AIOBoto3Client:
    """Singleton class to manage aioboto3 session and client."""

    client = aioboto3.Session().client(
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )

    async def get_client(self):
        async with self.client as client:
            client: S3Client
            yield client


boto_client_helper = AIOBoto3Client()
