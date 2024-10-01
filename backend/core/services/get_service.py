from functools import lru_cache
from typing import Type, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from types_aiobotocore_s3 import S3Client

from core.db_helper import db_helper
from app import app
from core.botoclient_helper import boto_client_helper


def get_service(service_class: Type) -> Callable:
    """
    Returns an instance of the `service_class` with the provided `pg` session.
    Parameters:
        pg (AsyncSession): The session to be used for the service. Defaults to the result of calling `db_helper.session_getter`.
        service_class (Type): The class of the service to be returned.
    Returns:
        object: An instance of the `service_class` with the provided `pg` session.
    Note:
        This function uses the `lru_cache` decorator to cache the results of previous calls with the same arguments.
    """

    @lru_cache()
    def service(pg: AsyncSession = Depends(db_helper.session_getter)):
        return service_class(pg=pg)

    return service


def get_s3_service(service_class: Type) -> Callable:
    @lru_cache()
    def dependency_getter(
        client: S3Client = Depends(boto_client_helper.get_client),
    ):
        return service_class(client=client)

    return dependency_getter
