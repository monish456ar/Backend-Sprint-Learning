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


class UserResponse(UserBase):
    """Schema for public user profile.

    Inherits `username` and `email` from UserBase, adds `role`.
    
    CRITICAL REQUIREMENT:
    Because `password` is only declared in UserRegister / UserLogin,
    UserResponse can never accidentally inherit or leak passwords.
    """
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    role: str = Field(..., description="User's platform role", examples=["admin"])
