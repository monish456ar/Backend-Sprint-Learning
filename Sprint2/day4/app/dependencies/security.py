from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from uuid import UUID
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from app.config import settings
from app.exceptions.domain_exceptions import InvalidTokenError, TokenExpiredError

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    """Hashes a plain-text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a bcrypt hash, with legacy fallback."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return plain_password == hashed_password


def create_access_token(
    user_id: UUID | str,
    role: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Creates a short-lived JWT access token for API authorization."""
    now = datetime.now(timezone.utc)
    expire = now + (
        expires_delta or timedelta(minutes=settings.token_expire_minutes)
    )
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(
        payload, settings.token_secret_key, algorithm=settings.token_algorithm
    )


def create_refresh_token(
    user_id: UUID | str,
    role: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Creates a long-lived JWT refresh token for renewing access tokens."""
    now = datetime.now(timezone.utc)
    expire = now + (
        expires_delta or timedelta(days=settings.refresh_token_expire_days)
    )
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "role": role,
        "type": "refresh",
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(
        payload, settings.token_secret_key, algorithm=settings.token_algorithm
    )


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decodes and verifies a JWT token.
    Raises TokenExpiredError if expired, or InvalidTokenError if malformed.
    """
    try:
        payload = jwt.decode(
            token,
            settings.token_secret_key,
            algorithms=[settings.token_algorithm],
        )
        return payload
    except ExpiredSignatureError as e:
        raise TokenExpiredError() from e
    except JWTError as e:
        raise InvalidTokenError() from e
