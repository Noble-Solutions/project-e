from fastapi import Form, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from .auth_utils import validate_password, decode_jwt
from .db_actions import get_user_by_username
from core.exceptions import unauthed_exc
from jwt.exceptions import JWTDecodeError
from backend_types import RoleType

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
)


def validate_auth_credentials_of_user(
    username: str = Form(),
    password: str = Form(),
) -> dict:
    if not (user := get_user_by_username(username)):
        raise unauthed_exc

    if not validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc
    user_schema_for_creating_access_token = {
        "username": user.username,
        "role_type": user.role_type,
    }
    return user_schema_for_creating_access_token


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = decode_jwt(
            token=token,
        )
    except JWTDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def check_access_by_token(
    role: RoleType,
    token: str = Depends(oauth2_scheme),
):
    payload = get_current_token_payload(token)
    if payload["role"] != role:
        raise unauthed_exc
    return True
