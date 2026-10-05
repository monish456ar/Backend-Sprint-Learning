from datetime import datetime, timezone
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, AliasChoices


class ReviewCreate(BaseModel):
    """Schema for creating a review with strict typing and field constraints."""
    model_config = ConfigDict(str_strip_whitespace=True)

    user_id: Optional[UUID] = Field(None, description="Optional user ID creating the review")
    rating: int = Field(..., ge=1, le=10, description="Integer rating between 1 and 10", examples=[9])
    review_body: str = Field(
        ...,
        min_length=50,
        description="Review body containing at least 50 characters",
        examples=["This masterpiece delivers exceptional storytelling, cinematography, and brilliant performances."],
    )


class ReviewUpdate(BaseModel):
    """Schema for updating an existing review."""
    model_config = ConfigDict(str_strip_whitespace=True)

    rating: Optional[float] = Field(None, ge=1, le=10, description="Rating between 1 and 10", examples=[8.9])
    review_body: Optional[str] = Field(None, min_length=50, description="Review body containing at least 50 characters")
    user_id: Optional[UUID] = Field(None, description="User ID for ownership verification")


class ReviewResponse(BaseModel):
    """Schema for review response."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID = Field(
        ...,
        validation_alias=AliasChoices("id", "review_id"),
        serialization_alias="id",
        description="Unique review identifier (UUID)",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    film_id: UUID = Field(..., description="UUID of the film", examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"])
    rating: float = Field(..., description="Rating given to the film", examples=[9.0])
    review_body: str = Field(..., description="Review body content")
    reviewer_name: str = Field(
        default="Anonymous Critic",
        validation_alias=AliasChoices("reviewer_name", "reviewer_display_name"),
        serialization_alias="reviewer_name",
        description="Reviewer display name",
        examples=["MovieBuff42"],
    )
    submission_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Review submission timestamp in UTC",
    )
