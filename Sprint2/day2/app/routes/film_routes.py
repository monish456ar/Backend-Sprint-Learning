from typing import Any, Dict, List
from fastapi import APIRouter, status
from app.handlers import film_handler
from app.schemas.film_schemas import FilmCreate, FilmUpdate, FilmResponse, FilmFilterQuery

router = APIRouter(prefix="/films", tags=["Films"])


@router.get("", response_model=List[FilmResponse], summary="Get all films")
def get_all_films() -> List[FilmResponse]:
    result = film_handler.handle_get_all_films()
    return result.get("data", [])


@router.get("/{film_id}", response_model=FilmResponse, summary="Get film by ID")
def get_film(film_id: int) -> FilmResponse:
    result = film_handler.handle_get_film(film_id)
    return result.get("data", result)


@router.post("", response_model=FilmResponse, status_code=status.HTTP_201_CREATED, summary="Create a new film")
def create_film(payload: FilmCreate) -> FilmResponse:
    result = film_handler.handle_create_film(payload.model_dump())
    return result["data"]


@router.post("/filter", response_model=List[FilmResponse], summary="Filter films by year range (Cross-field validation)")
def filter_films(payload: FilmFilterQuery) -> List[FilmResponse]:
    result = film_handler.handle_filter_films(payload.model_dump())
    return result.get("data", [])


@router.patch("/{film_id}", response_model=FilmResponse, summary="Update a film")
def update_film(film_id: int, payload: FilmUpdate) -> FilmResponse:
    result = film_handler.handle_update_film(film_id, payload.model_dump(exclude_unset=True))
    return result["data"]


@router.delete("/{film_id}", summary="Delete a film")
def delete_film(film_id: int) -> Dict[str, Any]:
    return film_handler.handle_delete_film(film_id)
