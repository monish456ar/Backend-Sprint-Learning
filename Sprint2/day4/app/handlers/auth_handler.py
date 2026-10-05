from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.domain_exceptions import UserAlreadyExistsError, UserNotFoundError
from app.models.user import User
from app.services import auth_service


async def handle_register(db: AsyncSession, user_data: Dict[str, Any]) -> User:
    """Registers a user, translating UserAlreadyExistsError into HTTP 400."""
    try:
        return await auth_service.register_user(db, user_data)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )


async def handle_login(
    db: AsyncSession, credentials: Dict[str, Any]
) -> Dict[str, Any]:
    """Authenticates user credentials."""
    data = await auth_service.login_user(db, credentials)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return data


async def handle_get_me(db: AsyncSession) -> User:
    """Retrieves current user profile."""
    user = await auth_service.get_current_user_profile(db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


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
