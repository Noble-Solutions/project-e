from fastapi import HTTPException
from jwt import InvalidTokenError
from sqlalchemy import select

from config import settings
from core.services.base_service import BaseService
from core.utils.auth_utils import (
    hash_password,
    encode_jwt,
    validate_password,
    decode_jwt,
)
from core.utils.exceptions import (
    user_already_exists_exc,
    unauthed_exc,
    user_not_found_exc,
)
from core.models import User
from core.schemas import UserCreateInDB, UserCreate
from core.schemas.user import UserRead

from core.schemas.user import AccessTokenPayload


class AuthService(BaseService):
    """
    В этом сервисе описаны все действия по работе с авторизацией
    которые вовлекают работы с базой данных.

    Все действия для которых не нужна работа с БД описаны в файле auth_utils
    в модуле utils
    """

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> UserRead:
        """
        Asynchronously retrieves a user by their ID, including role-specific fields.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            UserRead: The user with the given ID, or None if not found.

        Raises:
            HTTPException: If there is an error retrieving the user from the database.
        """
        stmt = select(User).where(User.id == user_id)
        user = await self.db.scalar(stmt)
        if not user:
            raise user_not_found_exc
        return UserRead.model_validate(user)

    async def get_user_by_username(
        self,
        username: str,
    ) -> UserRead | None:
        """
        Asynchronously retrieves a user by their username, including role-specific fields.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            Teacher | Student | None: The user with the given username, or None if not found.
        """
        stmt = select(User).where(User.username == username)
        user = await self.db.scalar(stmt)
        return user

    async def _add_user_to_db(
        self,
        user: UserCreateInDB,
    ):
        """
        Asynchronously adds a user to the database.

        Args:
            user (UserCreateInDB): The user object to be added to the database.

        Returns:
            User: The added user object.

        Raises:
            HTTPException: If there is an error adding the user to the database.
        """
        user = User(**user.model_dump())
        self.db.add(user)
        await self.db.commit()
        return user

    async def _validate_auth_credentials_of_user(
        self,
        username: str,
        password: str,
    ) -> AccessTokenPayload:
        """
        Asynchronously validates the authentication credentials of a user.

        This method takes in a username and a password as parameters and checks if the provided credentials are valid.
        It first retrieves the user from the database using the provided username. If the user does not exist,
        it raises an unauthenticated exception.
        Next, it validates the password by comparing it with the hashed password stored in the user object.
        If the password is incorrect, it also raises an unauthenticated exception. Finally, it creates a user schema
        for creating an access token and returns it.

        Parameters:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            AccessTokenPayload: The user schema for creating an access token.

        Raises:
            unauthed_exc: If the user does not exist or the password is incorrect.
        """
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
            subject=user.subject,
        )
        return user_schema_for_creating_access_token

    async def register_new_user(
        self,
        user: UserCreate,
    ) -> UserRead:
        """
        Asynchronously registers a new user.

        This method takes in a `UserCreate` object representing the user to be registered.
        It first checks if a user with the same username already exists in the database.
        If a user already exists, it raises a 'user_already_exists_exc` exception.
        If the user passes the validation checks, the method hashes the user's password using the `hash_password` function.
        It then adds the user to the database by calling the `_add_user_to_db` method with a `UserCreateInDB`
        object containing the user's data and the hashed password.

        Finally, it returns a UserRead object

        Parameters:
            user (UserCreate): The user object to be registered.

        Returns:
            UserRead: The registered user, or None if registration fails.

        Raises:
            user_already_exists_exc: If a user with the same username already exists in the database.
            invalid_data_for_register_exc: If the user's data is invalid for registration.
        """
        user_from_db = await self.get_user_by_username(user.username)

        if user_from_db:
            raise user_already_exists_exc

        hashed_password = hash_password(user.password)

        user = await self._add_user_to_db(
            UserCreateInDB(
                **user.model_dump(exclude_unset=True),
                hashed_password=hashed_password,
            )
        )

        return UserRead.model_validate(user)

    async def login_user(self, username: str, password: str):
        """
        Login a user and return access and refresh tokens.
        """
        user_schema = await self._validate_auth_credentials_of_user(username, password)
        access_token = encode_jwt(
            payload=user_schema,
            expire_minutes=settings.auth_jwt.access_token_expire_minutes,
        )
        refresh_token = encode_jwt(
            payload=user_schema,
            expire_minutes=settings.auth_jwt.refresh_token_expire_minutes,
        )
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def refresh_access_token(self, refresh_token: str):
        """
        Refresh the access token using the refresh token.
        """
        try:
            payload = decode_jwt(refresh_token)
            user_schema = AccessTokenPayload.model_validate(payload)
            new_access_token = encode_jwt(
                payload=user_schema,
                expire_minutes=settings.auth_jwt.access_token_expire_minutes,
            )
            return new_access_token
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
