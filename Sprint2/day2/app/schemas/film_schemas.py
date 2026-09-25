from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, AliasChoices, computed_field, model_validator


class FilmCreate(BaseModel):
    """Schema for creating a new film with strict validation."""
    model_config = ConfigDict(strict=True, str_strip_whitespace=True)

    title: str = Field(..., min_length=1, max_length=150, description="Title of the film", examples=["Inception"])
    release_year: int = Field(..., ge=1888, le=2100, description="Year film was released", examples=[2010])
    genre: str = Field(..., min_length=1, max_length=50, description="Film genre", examples=["Sci-Fi"])
    director: str = Field(..., min_length=1, max_length=100, description="Director of the film", examples=["Christopher Nolan"])


class FilmUpdate(BaseModel):
    """Schema for updating film details with strict validation."""
    model_config = ConfigDict(strict=True, str_strip_whitespace=True)

    title: Optional[str] = Field(None, min_length=1, max_length=150, examples=["Inception Updated"])
    release_year: Optional[int] = Field(None, ge=1888, le=2100, examples=[2010])
    genre: Optional[str] = Field(None, min_length=1, max_length=50, examples=["Sci-Fi / Action"])
    director: Optional[str] = Field(None, min_length=1, max_length=100, examples=["Christopher Nolan"])


class FilmResponse(BaseModel):
    """Schema for film response including @computed_field for years_ago."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int = Field(
        ...,
        validation_alias=AliasChoices("id", "film_id"),
        serialization_alias="id",
        description="Generated unique film identifier",
        examples=[1],
    )
    title: str = Field(..., description="Title of the film", examples=["Inception"])
    release_year: int = Field(..., description="Year film was released", examples=[2010])
    genre: str = Field(..., description="Film genre", examples=["Sci-Fi"])
    director: str = Field(..., description="Film director", examples=["Christopher Nolan"])

    @computed_field
    @property
    def years_ago(self) -> int:
        """Derived field calculating how many years ago the film was released."""
        current_year = datetime.now(timezone.utc).year
        return max(0, current_year - self.release_year)


class FilmFilterQuery(BaseModel):
    """Schema demonstrating cross-field validation with @model_validator."""
    model_config = ConfigDict(strict=True)

    start_year: int = Field(..., ge=1888, description="Start year of the filter range", examples=[1990])
    end_year: int = Field(..., le=2100, description="End year of the filter range", examples=[2020])

    @model_validator(mode="after")
    def validate_year_range(self) -> "FilmFilterQuery":
        if self.start_year > self.end_year:
            raise ValueError("start_year must be less than or equal to end_year")
        return self
