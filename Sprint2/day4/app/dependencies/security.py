import base64
from datetime import datetime, timedelta, timezone
import json
from typing import Any, Dict, Optional, Tuple
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


def encode_film_cursor(created_at: datetime, film_id: UUID) -> str:
    """Encodes created_at and film_id into an opaque URL-safe base64 string."""
    payload = json.dumps({"ts": created_at.isoformat(), "id": str(film_id)})
    return base64.urlsafe_b64encode(payload.encode("utf-8")).decode("utf-8")


def decode_film_cursor(cursor_str: str) -> Tuple[datetime, UUID]:
    """Decodes an opaque base64 string back to (created_at, film_id)."""
    try:
        raw = base64.urlsafe_b64decode(cursor_str.encode("utf-8")).decode("utf-8")
        data = json.loads(raw)
        return datetime.fromisoformat(data["ts"]), UUID(data["id"])
    except Exception as exc:
        raise ValueError(f"Invalid cursor token: {exc}") from exc
