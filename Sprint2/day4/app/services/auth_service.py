import logging
from typing import Any, Dict, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.dao.user_dao import UserDAO
from app.exceptions.domain_exceptions import (
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    UserAlreadyExistsError,
)
from app.models.user import User
from app.dependencies.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
)


logger = logging.getLogger("app.auth_service")


async def register_user(db: AsyncSession, user_data: Dict[str, Any]) -> User:
    """
    Registers a new user after verifying unique email and username,
    and securely hashing the password using bcrypt.
    """
    existing_by_email = await UserDAO.get_user_by_email(db, user_data["email"])
    if existing_by_email:
        raise UserAlreadyExistsError("email", user_data["email"])

    existing_by_username = await UserDAO.get_user_by_username(db, user_data["username"])
    if existing_by_username:
        raise UserAlreadyExistsError("username", user_data["username"])

    # Securely hash password with bcrypt before persistence
    data_to_save = dict(user_data)
    data_to_save["password"] = hash_password(user_data["password"])

    user = await UserDAO.create_user(db, data_to_save)
    logger.info("Registered user %s (id=%s)", user.username, user.id)
    return user


async def login_user(
    db: AsyncSession, credentials: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Validates user credentials against bcrypt hash and issues
    both a short-lived access token and a long-lived refresh token.
    """
    user = await UserDAO.authenticate_user(db, credentials)
    if not user:
        raise InvalidCredentialsError()

    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id, user.role)

    logger.info("Issued JWT tokens for user %s (role=%s)", user.username, user.role)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.token_expire_minutes * 60,
    }


async def refresh_access_token(
    db: AsyncSession, refresh_token: str
) -> Dict[str, Any]:
    """
    Validates a JWT refresh token and issues a new access token and refresh token.
    Rejects expired, malformed, or non-refresh tokens.
    """
    try:
        payload = decode_token(refresh_token)
    except Exception as e:
        logger.warning("Failed to decode refresh token: %s", str(e))
        raise InvalidRefreshTokenError("Invalid or expired refresh token.") from e

    token_type = payload.get("type")
    if token_type != "refresh":
        logger.warning("Token provided to /refresh is not of type 'refresh': %s", token_type)
        raise InvalidRefreshTokenError("Provided token is not a refresh token.")

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise InvalidRefreshTokenError("Token payload missing subject identifier.")

    try:
        user_uuid = UUID(user_id_str)
    except (ValueError, TypeError) as e:
        raise InvalidRefreshTokenError("Invalid user identifier in refresh token.") from e

    user = await UserDAO.get_user_by_id(db, user_uuid)
    if not user:
        raise InvalidRefreshTokenError("User associated with refresh token no longer exists.")

    new_access_token = create_access_token(user.id, user.role)
    new_refresh_token = create_refresh_token(user.id, user.role)

    logger.info("Successfully refreshed tokens for user %s", user.username)
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": settings.token_expire_minutes * 60,
    }


async def get_current_user_profile(db: AsyncSession, user: Optional[User] = None) -> Optional[User]:
    """Retrieves current user profile."""
    if user:
        return user
    return await UserDAO.get_current_user(db)


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Finds user by email via UserDAO."""
    return await UserDAO.get_user_by_email(db, email)


async def get_platform_admin_stats(db: AsyncSession) -> Dict[str, Any]:
    """Calculates administrative stats via UserDAO."""
    return await UserDAO.get_admin_stats(db)

