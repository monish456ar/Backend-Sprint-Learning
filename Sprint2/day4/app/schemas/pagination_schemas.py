from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field, model_validator

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Offset-based pagination parameters."""
    model_config = ConfigDict(extra="ignore")

    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=10, ge=1, le=100, description="Records requested per page (max 100)")


class CursorPaginationParams(BaseModel):
    """Cursor-based pagination parameters."""
    model_config = ConfigDict(extra="ignore")

    cursor: Optional[str] = Field(default=None, description="Opaque cursor token for the next batch")
    limit: int = Field(default=10, ge=1, le=100, description="Number of items to fetch per batch (max 100)")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic envelope for offset-paginated responses."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, description="Number of records requested per page")
    total: int = Field(..., ge=0, description="Total number of matching records")
    items: List[T] = Field(..., description="Records belonging to the requested page")


class CursorPaginatedResponse(BaseModel, Generic[T]):
    """Generic envelope for cursor-paginated responses."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    items: List[T] = Field(..., description="Records in the current batch")
    next_cursor: Optional[str] = Field(default=None, description="Opaque cursor to fetch the next batch, or null if no more records")


class FilmFilterParams(BaseModel):
    """Validated multi-field filter parameters for film listing."""
    model_config = ConfigDict(extra="ignore")

    genre: Optional[str] = Field(default=None, min_length=1, max_length=50, description="Exact genre match")
    from_year: Optional[int] = Field(default=None, ge=1888, le=2100, description="Minimum release year")
    to_year: Optional[int] = Field(default=None, ge=1888, le=2100, description="Maximum release year")
    director: Optional[str] = Field(default=None, min_length=1, max_length=100, description="Case-insensitive substring match on director")

    @model_validator(mode="after")
    def validate_year_range(self) -> "FilmFilterParams":
        if self.from_year is not None and self.to_year is not None and self.from_year > self.to_year:
            raise ValueError("from_year must be less than or equal to to_year")
        return self


class ReviewFilterParams(BaseModel):
    """Validated filter parameters for film review listing."""
    model_config = ConfigDict(extra="ignore")

    min_rating: Optional[int] = Field(default=None, ge=1, le=10, description="Minimum rating (1-10)")
    max_rating: Optional[int] = Field(default=None, ge=1, le=10, description="Maximum rating (1-10)")

    @model_validator(mode="after")
    def validate_rating_range(self) -> "ReviewFilterParams":
        if self.min_rating is not None and self.max_rating is not None and self.min_rating > self.max_rating:
            raise ValueError("min_rating must be less than or equal to max_rating")
        return self

