from typing import Optional
from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5, example=5)
    comment: str = Field(..., example="Amazing cinematic experience!")


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5, example=4)
    comment: Optional[str] = Field(None, example="Revised review comment.")
