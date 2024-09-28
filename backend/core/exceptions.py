from fastapi import HTTPException
from starlette import status
from .constants import invalid_auth_credentials


invalid_data_for_register_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Неправильные данные для регистрации",
)

student_already_in_classroom_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Ученик уже в этом классе",
)

unauthed_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неправильные имя пользователя или пароль",
)

forbidden_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Доступ запрещен",
)

user_already_exists_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Пользователь с таким именем пользователя уже существует",
)
