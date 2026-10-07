import logging
from typing import Optional
from uuid import UUID
from fastapi import Depends, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.user_dao import UserDAO
from app.dependencies.db_deps import get_db
from app.exceptions.domain_exceptions import (
    AccessDeniedException,
    InvalidTokenError,
    MissingTokenError,
    UserNotFoundError,
)
from app.models.user import User
from app.dependencies.security import decode_token

logger = logging.getLogger("app.auth")


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False,
)


async def token_validator(
    token: Optional[str] = Depends(oauth2_scheme),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    FastAPI token validator & authentication dependency.
    Accepts raw token directly (without 'Bearer') or with 'Bearer <token>'.
    Validates the JWT token and resolves the authenticated User from PostgreSQL.
    """
    raw_token = token or authorization
    if not raw_token:
        logger.warning("Rejected unauthenticated request: missing Authorization header")
        raise MissingTokenError()

    # Clean token: remove 'Bearer ' prefix if present, and trim whitespace/quotes
    clean_token = raw_token.strip()
    if clean_token.lower().startswith("bearer "):
        clean_token = clean_token[7:].strip()
    clean_token = clean_token.strip("\"'<> \t\r\n")

    try:
        payload = decode_token(clean_token)
        print("payload - ", payload)
    except Exception as e:
        logger.warning("Token verification failed: %s", str(e))
        raise

    token_type = payload.get("type")
    if token_type != "access":
        logger.warning("Rejected token: type is '%s' (expected 'access')", token_type)
        raise InvalidTokenError("Token is not an access token. Ensure you are sending the access_token, not refresh_token.")

    user_id_str = payload.get("sub")
    if not user_id_str:
        logger.warning("Rejected token: missing 'sub' claim")
        raise InvalidTokenError("Token missing subject identifier.")

    try:
        user_uuid = UUID(user_id_str)
    except (ValueError, TypeError) as e:
        logger.warning("Rejected token: malformed UUID '%s'", user_id_str)
        raise InvalidTokenError("Token subject is not a valid UUID.") from e

    user = await UserDAO.get_user_by_id(db, user_uuid)
    if not user:
        logger.warning("Rejected token: user UUID '%s' not found in database", user_uuid)
        raise UserNotFoundError(user_id_str, "User not found.")

    return user


def require_role(*allowed_roles: str):
    """
    Role-based access control dependency factory.
    Verifies that the authenticated user has one of the allowed roles.
    Raises AccessDeniedException if unauthorized.
    """
    async def role_checker(user: User = Depends(token_validator)) -> User:
        if user.role not in allowed_roles:
            logger.warning(
                "Access denied for user %s (role='%s'): required role in %s",
                user.id,
                user.role,
                allowed_roles,
            )
            raise AccessDeniedException(user.role)
        return user

    return role_checker
