from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    """Shared public identity fields for user models."""
    username: str = Field(..., min_length=1, description="User's username", examples=["monish"])
    email: str = Field(..., min_length=3, description="User's email address", examples=["monish@gmail.com"])


class UserLogin(BaseModel):
    """Schema for user authentication credentials."""
    model_config = ConfigDict(strict=True, str_strip_whitespace=True)

    username: str = Field(..., min_length=1, description="User's username", examples=["monish"])
    password: str = Field(..., min_length=6, description="User's password", examples=["secret123"])


class UserRegister(UserBase):
    """Registration schema inheriting username & email from UserBase, adding password."""
    model_config = ConfigDict(strict=True, str_strip_whitespace=True)

    password: str = Field(..., min_length=6, description="User's password", examples=["secret123"])
    role: str = Field(default="user", description="User's platform role", examples=["user"])


class UserResponse(UserBase):
    """Schema for public user profile.

    Inherits `username` and `email` from UserBase, adds `id` and `role`.
    
    CRITICAL REQUIREMENT:
    Because `password` is only declared in UserRegister / UserLogin,
    UserResponse can never accidentally inherit or leak passwords.
    """
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: UUID = Field(..., description="User's unique identifier")
    role: str = Field(..., description="User's platform role", examples=["admin"])


class TokenResponse(BaseModel):
    """Schema for JWT authentication response containing access and refresh tokens."""
    access_token: str = Field(..., description="Short-lived JWT access token")
    refresh_token: str = Field(..., description="Long-lived JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Access token expiration window in seconds")


class TokenRefreshRequest(BaseModel):
    """Schema for requesting a new access token using a valid refresh token."""
    model_config = ConfigDict(strict=True, str_strip_whitespace=True)

    refresh_token: str = Field(..., min_length=1, description="JWT refresh token")

