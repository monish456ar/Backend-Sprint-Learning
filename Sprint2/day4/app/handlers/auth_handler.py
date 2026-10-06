from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.domain_exceptions import UserAlreadyExistsError, UserNotFoundError
from app.models.user import User
from app.services import auth_service


async def handle_register(db: AsyncSession, user_data: Dict[str, Any]) -> User:
    """Registers a new user, delegating to auth_service."""
    return await auth_service.register_user(db, user_data)


async def handle_login(
    db: AsyncSession, credentials: Dict[str, Any]
) -> Dict[str, Any]:
    """Authenticates credentials and returns access and refresh tokens."""
    return await auth_service.login_user(db, credentials)


async def handle_refresh(
    db: AsyncSession, refresh_token: str
) -> Dict[str, Any]:
    """Validates refresh token and returns refreshed access and refresh tokens."""
    return await auth_service.refresh_access_token(db, refresh_token)


async def handle_get_me(current_user: User) -> User:
    """Returns the authenticated user entity directly."""
    return current_user



async def handle_get_user_by_email(db: AsyncSession, email: str) -> User:
    """Retrieves user by email address."""
    user = await auth_service.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{email}' not found",
        )
    return user


async def handle_get_admin_stats(db: AsyncSession) -> Dict[str, Any]:
    """Calculates live administrative stats."""
    return await auth_service.get_platform_admin_stats(db)
