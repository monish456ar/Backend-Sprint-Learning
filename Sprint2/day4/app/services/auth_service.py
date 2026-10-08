import logging
from typing import Any, Dict, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.dao.user_dao import UserDAO
from app.database.redis_client import redis_client
from app.exceptions.domain_exceptions import (
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.models.user import User
from app.dependencies.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
)

logger = logging.getLogger("app.auth_service")


async def store_refresh_token(
    user_id: UUID | str, refresh_token: str, ttl_seconds: int
) -> None:
    """Stores the active refresh token in Redis with a TTL matching token expiry."""
    user_key = f"refresh_token:{user_id}"
    token_key = f"token:{refresh_token}"

    try:
        # Invalidate any previously tracked token for this user
        old_token = await redis_client.get(user_key)
        if old_token and old_token != refresh_token:
            await redis_client.delete(f"token:{old_token}")

        await redis_client.set(user_key, refresh_token, ex=ttl_seconds)
        await redis_client.set(token_key, str(user_id), ex=ttl_seconds)
        logger.debug(
            "Stored refresh token in Redis for user %s with TTL %ds",
            user_id,
            ttl_seconds,
        )
    except Exception as e:
        logger.warning("Redis write error when storing refresh token: %s", str(e))


async def get_refresh_token(user_id: UUID | str) -> Optional[str]:
    """Retrieves the active refresh token for a user from Redis."""
    try:
        return await redis_client.get(f"refresh_token:{user_id}")
    except Exception as e:
        logger.warning("Redis read error when getting refresh token: %s", str(e))
        return None


async def revoke_refresh_token(user_id: UUID | str) -> None:
    """Explicitly deletes the user's refresh token from Redis upon logout."""
    user_key = f"refresh_token:{user_id}"
    try:
        token = await redis_client.get(user_key)
        if token:
            await redis_client.delete(f"token:{token}")
        await redis_client.delete(user_key)
        logger.info("Revoked refresh token from Redis for user %s", user_id)
    except Exception as e:
        logger.warning("Redis delete error when revoking refresh token: %s", str(e))


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
    Validates user credentials against bcrypt hash, issues both access and refresh tokens,
    and stores the refresh token in Redis with a TTL matching the token expiry.
    """
    user = await UserDAO.authenticate_user(db, credentials)
    if not user:
        raise InvalidCredentialsError()

    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id, user.role)
    refresh_ttl = settings.refresh_token_expire_days * 86400

    # Store refresh token in Redis with matching TTL
    await store_refresh_token(user.id, refresh_token, refresh_ttl)

    logger.info("Issued and stored JWT tokens for user %s (role=%s)", user.username, user.role)
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
    Validates a JWT refresh token, verifies it exists in Redis (rejecting revoked or logged-out tokens),
    and issues a new pair of access and refresh tokens, updating Redis storage.
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

    # Check Redis for the active refresh token.
    # If the user logged out, the token will be missing from Redis and rejected.
    stored_token = await get_refresh_token(user_uuid)
    if not stored_token or stored_token != refresh_token:
        logger.warning("Refresh token for user %s not found in Redis or has been revoked", user_uuid)
        raise InvalidRefreshTokenError("Refresh token has been revoked or expired.")

    user = await UserDAO.get_user_by_id(db, user_uuid)
    if not user:
        raise InvalidRefreshTokenError("User associated with refresh token no longer exists.")

    new_access_token = create_access_token(user.id, user.role)
    new_refresh_token = create_refresh_token(user.id, user.role)
    refresh_ttl = settings.refresh_token_expire_days * 86400

    # Store newly issued refresh token in Redis
    await store_refresh_token(user.id, new_refresh_token, refresh_ttl)

    logger.info("Successfully refreshed tokens for user %s", user.username)
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": settings.token_expire_minutes * 60,
    }


async def logout_user(user_id: UUID | str) -> Dict[str, Any]:
    """
    Logs out the caller and explicitly deletes their refresh token from Redis.
    Subsequent attempts to use the revoked refresh token will be rejected.
    """
    await revoke_refresh_token(user_id)
    logger.info("User %s logged out and refresh token revoked from Redis", user_id)
    return {"message": "User logged out successfully", "status": "success"}


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


async def delete_user(db: AsyncSession, user_id: UUID) -> bool:
    """Deletes user by ID. Raises UserNotFoundError if user does not exist."""
    user = await UserDAO.get_user_by_id(db, user_id)
    if not user:
        raise UserNotFoundError(str(user_id))

    # Also clean up any refresh token from Redis
    await revoke_refresh_token(user_id)

    deleted = await UserDAO.delete_user(db, user_id)
    if not deleted:
        raise UserNotFoundError(str(user_id))

    logger.info("Admin deleted user %s (id=%s)", user.username, user_id)
    return True
