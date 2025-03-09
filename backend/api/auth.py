from fastapi import APIRouter, Depends, Form

from core.utils.auth_utils import get_current_token_payload
from core.services.get_service import get_service
from core.services.auth import AuthService
from core.schemas.user import UserCreate, UserRead
from fastapi.security import HTTPBearer
from fastapi import Response, Cookie, HTTPException

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", status_code=201)
async def register(
    user: UserCreate,
    auth_service: AuthService = Depends(get_service(AuthService)),
):
    """
    Register a new user.

    Args:
        user (UserCreate): The user url_fields_dictionary to be registered.
        auth_service (AuthService): The authentication service dependency. Defaults to the result of calling `get_service(AuthService)`.

    Returns:
        UserRead: The registered user's url_fields_dictionary.

    Raises:
            user_already_exists_exc: If a user with the same username already exists in the database.
            invalid_data_for_register_exc: If the user's data is invalid for registration.
    """
    return await auth_service.register_new_user(user)


@router.post("/login")
async def login(
    response: Response,
    auth_service: AuthService = Depends(get_service(AuthService)),
    username: str = Form(...),
    password: str = Form(...),
):
    """
    Login a user and set access and refresh tokens in cookies.
    """
    tokens = await auth_service.login_user(username, password)
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=False,  # TODO обязательно поменять на true когда перейду на htpps
        samesite="none",
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=False,
        samesite="none",
    )
    return {"message": "Logged in successfully"}


@router.post("/logout")
async def logout(response: Response):
    """
    Logout the user by deleting access and refresh tokens from cookies.
    """
    # Удаляем access_token
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,
        samesite="none",
    )

    # Удаляем refresh_token
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,
        samesite="none",
    )

    return {"message": "Logged out successfully"}


@router.post("/refresh")
async def refresh_access_token(
    response: Response,
    refresh_token: str = Cookie(None),
    auth_service: AuthService = Depends(get_service(AuthService)),
):
    """
    Refresh the access token using the refresh token.
    """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token is missing")

    new_access_token = await auth_service.refresh_access_token(refresh_token)
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,
        samesite="none",
    )
    return {"access_token": new_access_token}


#


@router.get("/me")
async def get_current_user(
    access_token: str = Cookie(None),
    user_schema: dict = Depends(get_current_token_payload),
):
    """
    Get the current user's schema using the access token from cookies.
    """
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token is missing")
    return user_schema
