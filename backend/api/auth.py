from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from core.auth.auth_utils import hash_password, encode_jwt
from core.auth.auth_validation import (
    validate_auth_credentials_of_user,
    get_current_token_payload,
)
from core.db_helper import db_helper, postgres_session
from core.schemas import UserCreate, UserCreateInDB
from core.auth.db_actions import (
    get_user_by_username,
    add_user_to_db,
)
from core.exceptions import UserAlreadyExists
from core.constants import user_already_exists
from fastapi import HTTPException
from fastapi.security import HTTPBearer

from core.schemas.user import TeacherRead, StudentRead

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(http_bearer)],
)


@router.post("/register")
async def register_new_user(
    user: UserCreate,
    db_session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
) -> TeacherRead | StudentRead | None:
    postgres_session.set(db_session)
    try:
        user_from_db = await get_user_by_username(user.username)
        if user_from_db:
            raise UserAlreadyExists
        hashed_password = hash_password(user.password)
        user = await add_user_to_db(
            UserCreateInDB(
                **user.dict(),
                hashed_password=hashed_password,
            )
        )
    except UserAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=user_already_exists,
        )

    if user.role_type == "teacher":
        return TeacherRead.model_validate(user)
    return StudentRead.model_validate(user)


@router.get("/login")
async def login(
    db_session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
    user_schema: dict = Depends(validate_auth_credentials_of_user),
):
    postgres_session.set(db_session)
    access_token = encode_jwt(
        payload=user_schema,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user(
    user_schema: dict = Depends(get_current_token_payload),
):
    return user_schema
