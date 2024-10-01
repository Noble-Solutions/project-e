from fastapi import APIRouter, Depends, Form

from core.utils.auth_utils import get_current_token_payload
from core.services.get_service import get_service
from core.services.auth import AuthService
from core.schemas import UserCreate
from fastapi.security import HTTPBearer
from core.schemas.user import TeacherRead, StudentRead

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(http_bearer)],
)


@router.post("/register")
async def register(
    user: UserCreate,
    auth_service: AuthService = Depends(lambda: get_service(AuthService)),
):
    """
    Register a new user.

    Args:
        user (UserCreate): The user data to be registered.
        auth_service (AuthService, optional): The authentication service dependency. Defaults to the result of calling `get_service(AuthService)`.

    Returns:
        TeacherRead | StudentRead | None: The registered user.

    Raise:
        HTTPException: If the user already exists.
    """
    return await auth_service.register_new_user(user)


@router.post("/login")
async def login(
    auth_service: AuthService = Depends(lambda: get_service(AuthService)),
    username: str = Form(...),
    password: str = Form(...),
):
    """
    Login a user.

    Args:
        auth_service (AuthService, optional): The authentication service dependency.
        username (str): The username of the user.
        password (str): The password of the user.
    Returns:
        dict: The user payload.
    Raise:
        HTTPException: If the user does not exist or the password is incorrect.
    """
    return await auth_service.login_user(username, password)


@router.get("/me")
async def get_current_user(user_schema: dict = Depends(get_current_token_payload)):
    """
    Get the current user's schema.

    This endpoint retrieves the current user's schema by decoding the JWT token and
    extracting the user's information. The user's schema is returned as a dictionary.

    Returns:
        dict: The user's schema.

    Raises:
        HTTPException: If the JWT token is invalid or cannot be decoded.
    """
    return user_schema
