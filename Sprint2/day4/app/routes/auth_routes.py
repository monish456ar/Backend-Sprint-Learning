from typing import Any, Dict
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import (
    authenticate_user,
    get_config,
    get_db,
    Settings,
)
from app.handlers import auth_handler

from app.models.user import User
from app.schemas.auth_schemas import (
    TokenRefreshRequest,
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)

router = APIRouter(tags=["Auth / Users"])


@router.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
)
async def register_user(
    payload: UserRegister,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    user = await auth_handler.handle_register(db, payload.model_dump())
    return user


@router.post(
    "/auth/login",
    response_model=TokenResponse,
    summary="User login (returns access and refresh tokens)",
)
async def login_user(
    payload: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    return await auth_handler.handle_login(db, payload.model_dump())



@router.post(
    "/auth/refresh",
    response_model=TokenResponse,
    summary="Refresh access token using a valid refresh token",
)
async def refresh_token(
    payload: TokenRefreshRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    return await auth_handler.handle_refresh(db, payload.refresh_token)


@router.get(
    "/users/me",
    response_model=UserResponse,
    summary="Get current user profile (Password safely omitted)",
)
async def get_current_user_profile(
    current_user: User = Depends(authenticate_user),
) -> UserResponse:
    return await auth_handler.handle_get_me(current_user)


@router.get(
    "/auth/me",
    response_model=UserResponse,
    summary="Get current user profile (alias for /users/me)",
)
async def get_current_user_profile_alias(
    current_user: User = Depends(authenticate_user),
) -> UserResponse:
    return await auth_handler.handle_get_me(current_user)



@router.get(
    "/users/by-email",
    response_model=UserResponse,
    summary="Find user by email",
)
async def get_user_by_email(
    email: str,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    return await auth_handler.handle_get_user_by_email(db, email)


@router.get(
    "/admin/stats",
    summary="Get platform admin statistics",
)
async def get_admin_stats(
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    return await auth_handler.handle_get_admin_stats(db)

