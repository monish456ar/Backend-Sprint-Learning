from typing import Optional
from pydantic import BaseModel, Field


class FilmCreate(BaseModel):
    title: str = Field(..., example="Inception")
    genre: Optional[str] = Field(None, example="Sci-Fi")
    release_year: Optional[int] = Field(None, example=2010)
    description: Optional[str] = Field(None, example="A thief who steals corporate secrets...")


class FilmUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Inception Updated")
    genre: Optional[str] = Field(None, example="Sci-Fi / Action")
    release_year: Optional[int] = Field(None, example=2010)
    description: Optional[str] = Field(None, example="Updated description...")


class FilmResponse(BaseModel):
    title: str = Field(..., example="Inception")
    genre: Optional[str] = Field(None, example="Sci-Fi")
    description: Optional[str] = Field(None, example="A thief who steals corporate secrets...")

