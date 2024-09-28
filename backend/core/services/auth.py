from fastapi import HTTPException

from sqlalchemy import select

from sqlalchemy.orm import with_polymorphic

from core.services.base_service import BaseService
from core.utils.auth_utils import (
    hash_password,
    encode_jwt,
    validate_password,
)
from core.exceptions import (
    user_already_exists_exc,
    unauthed_exc,
    invalid_data_for_register_exc,
)
from core.models import Teacher, Student, User
from core.schemas import UserCreateInDB, UserCreate
from core.schemas.user import TeacherRead, StudentRead, UserRead

from core.schemas.user import AccessTokenPayload


class AuthService(BaseService):
    """
    В этом сервисе описаны все действия по работе с авторизацией
    которые вовлекают работы с базой данных.

    Все действия для которых не нужна работа с БД описаны в файле auth_utils
    в модуле auth
    """

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> Teacher | Student | None:
        # Fetch user with polymorphic loading to include role-specific fields
        user_polymorphic = with_polymorphic(User, [Teacher, Student])
        stmt = select(user_polymorphic).where(user_polymorphic.id == user_id)
        user = await self.db.scalar(stmt)
        return user

    async def get_user_by_username(
        self,
        username: str,
    ) -> Teacher | Student | None:
        # Fetch user with polymorphic loading to include role-specific fields
        user_polymorphic = with_polymorphic(User, [Teacher, Student])
        stmt = select(user_polymorphic).where(user_polymorphic.username == username)
        user = await self.db.scalar(stmt)
        print(user)
        return user

    async def _add_user_to_db(
        self,
        user: UserCreateInDB,
    ):
        try:
            print(user.model_dump())
            if user.role_type == "teacher":
                user = Teacher(**user.model_dump())
            if user.role_type == "student":
                user = Student(**user.model_dump(exclude_unset=True))
            self.db.add(user)
            await self.db.commit()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )
        return user

    async def _validate_auth_credentials_of_user(
        self,
        username: str,
        password: str,
    ) -> AccessTokenPayload:
        print(f"username= {str(username)}")
        if not (user := await self.get_user_by_username(str(username))):
            raise unauthed_exc
        if not validate_password(
            password=password,
            hashed_password=user.hashed_password,
        ):
            raise unauthed_exc
        user_schema_for_creating_access_token = AccessTokenPayload(
            id=user.id,
            username=user.username,
            role_type=user.role_type,
        )
        return user_schema_for_creating_access_token

    async def register_new_user(
        self,
        user: UserCreate,
    ) -> TeacherRead | StudentRead | None:
        user_from_db = await self.get_user_by_username(user.username)

        if user_from_db:
            raise user_already_exists_exc

        if user.role_type == "teacher":
            if "subject" not in user.model_dump(exclude_unset=True).keys():
                raise invalid_data_for_register_exc

        if user.role_type == "student":
            if "subject" in user.model_dump(exclude_unset=True).keys():
                raise invalid_data_for_register_exc

        hashed_password = hash_password(user.password)

        user = await self._add_user_to_db(
            UserCreateInDB(
                **user.model_dump(exclude_unset=True),
                hashed_password=hashed_password,
            )
        )

        if user.role_type == "teacher":
            return TeacherRead.model_validate(user)
        return StudentRead.model_validate(user)

    async def login_user(self, username: str, password: str):
        user_schema = await self._validate_auth_credentials_of_user(username, password)
        access_token = encode_jwt(
            payload=user_schema,
        )
        return {"access_token": access_token, "token_type": "bearer"}
