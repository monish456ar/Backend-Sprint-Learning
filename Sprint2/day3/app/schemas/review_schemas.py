from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, AliasChoices


class ReviewCreate(BaseModel):
    """Schema for creating a review with strict typing and field constraints."""
    model_config = ConfigDict(strict=True, str_strip_whitespace=True)

    film_id: int = Field(..., description="ID of the film being reviewed", examples=[1])
    rating: int = Field(..., ge=1, le=10, description="Strict integer rating between 1 and 10", examples=[9])
    review_body: str = Field(
        ...,
        min_length=50,
        description="Review body containing at least 50 characters",
        examples=["This masterpiece delivers exceptional storytelling, cinematography, and brilliant performances."],
    )


class ReviewUpdate(BaseModel):
    """Schema for updating an existing review with strict typing."""
    model_config = ConfigDict(strict=True, str_strip_whitespace=True)

    rating: Optional[int] = Field(None, ge=1, le=10, description="Strict integer rating between 1 and 10", examples=[8])
    review_body: Optional[str] = Field(None, min_length=50, description="Review body containing at least 50 characters")


class ReviewResponse(BaseModel):
    """Schema for review response."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int = Field(
        ...,
        validation_alias=AliasChoices("id", "review_id"),
        serialization_alias="id",
        description="Unique review identifier",
        examples=[101],
    )
    film_id: int = Field(..., description="ID of the film", examples=[1])
    rating: int = Field(..., description="Rating given to the film", examples=[9])
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
