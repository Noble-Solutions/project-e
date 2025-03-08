import uuid
from datetime import datetime, timedelta
from typing import List, Literal, Callable

import bcrypt
from fastapi import HTTPException, Depends, Cookie
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from jwt import InvalidTokenError
from jwt.api_jwt import encode
from jwt.api_jwt import decode
from starlette import status

from backend_types import RoleType
from config import settings
from core.utils.exceptions import forbidden_exc
from core.schemas.user import AccessTokenPayload


def encode_jwt(
    payload: dict | AccessTokenPayload,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    """
    Encodes a payload into a JSON Web Token (JWT) using the specified private key, algorithm, and expiration time.

    Args:
        payload (dict): The payload to be encoded.
        private_key (str, optional): The private key used for signing the JWT. Defaults to the value specified in the settings.auth_jwt.private_key_path.
        algorithm (str, optional): The algorithm used for signing the JWT. Defaults to the value specified in the settings.auth_jwt.algorithm.
        expire_minutes (int, optional): The expiration time of the JWT in minutes. Defaults to the value specified in the settings.auth_jwt.access_token_expire_minutes.
        expire_timedelta (timedelta | None, optional): The expiration time of the JWT as a timedelta object. Defaults to None.

    Returns:
        str: The encoded JWT.

    Raises:
        None

    """
    if isinstance(payload, AccessTokenPayload):
        payload = jsonable_encoder(payload)
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
        jti=str(uuid.uuid4()),
    )
    encoded = encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> AccessTokenPayload:
    """
    Decodes a JSON Web Token (JWT) using the specified public key and algorithm.

    Args:
        token (str | bytes): The JWT to be decoded.
        public_key (str, optional): The public key used for verifying the JWT. Defaults to the value specified in the settings.auth_jwt.public_key_path.
        algorithm (str, optional): The algorithm used for verifying the JWT. Defaults to the value specified in the settings.auth_jwt.algorithm.

    Returns:
        dict: The decoded payload of the JWT.

    Raises:
        InvalidTokenError: If the token is invalid or cannot be decoded.

    """
    decoded = decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return AccessTokenPayload.model_validate(decoded)


def hash_password(
    password: str,
) -> bytes:
    """
    Hashes a password using the bcrypt algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.

    """
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    """
    Validates a password by comparing it with a hashed password.

    Args:
        password (str): The plaintext password to be validated.
        hashed_password (bytes): The hashed password to compare against.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


def get_current_token_payload(
    access_token: str = Cookie(None),
) -> AccessTokenPayload:
    """
    Retrieves the payload of the current token from cookies.
    """
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token is missing")
    try:
        payload = decode_jwt(token=access_token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token error: {e}")
    return payload


def _check_access_by_token(
    roles: List[RoleType] | Literal["any"],
) -> Callable[[str], AccessTokenPayload]:
    """
    Checks if the user has the required roles based on the provided token.

    Args:
        roles (List[RoleType]): A list of roles that the user is expected to have.

    Returns:
        Callable: A dependency function that checks the user's roles.

    Raises:
        HTTPException: If the token is missing or invalid.
        forbidden_exc: If the user does not have the required roles.
    """

    def dependency(access_token: str = Cookie(None)):
        # Если токен отсутствует в cookies, выбрасываем исключение
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token is missing",
            )

        # Получаем payload из токена
        payload = get_current_token_payload(access_token)

        # Если roles == "any", возвращаем payload без проверки ролей
        if roles == "any":
            return payload

        # Проверяем, есть ли у пользователя необходимая роль
        if payload.role_type not in roles:
            raise forbidden_exc

        return payload

    return dependency


"""
Три переменные ниже нужны для использования в Depends так как в 
Depends нельзя передавать аргументы, так что мы создаем переменную куда присваиваем
функцию с аргументом
"""
get_current_teacher = _check_access_by_token(roles=["teacher"])
get_current_student = _check_access_by_token(roles=["student"])
get_current_user = _check_access_by_token(roles="any")
