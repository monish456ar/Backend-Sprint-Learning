from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    username: str = Field(..., example="john_doe")
    password: str = Field(..., example="secret123")

class UserRegister(UserLogin):
    # username: str = Field(..., example="john_doe")
    email: str = Field(..., example="john@example.com")
    # password: str = Field(..., min_length=6, example="secret123")





