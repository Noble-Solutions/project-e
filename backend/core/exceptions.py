from fastapi import HTTPException
from starlette import status
from .constants import invalid_auth_credentials


class UserAlreadyExists(Exception):
    pass


unauthed_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=invalid_auth_credentials,
)
