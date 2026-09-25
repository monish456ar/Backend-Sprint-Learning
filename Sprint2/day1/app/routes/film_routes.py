from typing import Any, Dict
from fastapi import APIRouter
from app.handlers import film_handler
from app.schemas.film_schemas import FilmCreate, FilmUpdate, FilmResponse

router = APIRouter(prefix="/films", tags=["Films"])


@router.get("", summary="Get all films")
def get_all_films() -> Dict[str, Any]:
    return film_handler.handle_get_all_films()


@router.get("/{film_id}", response_model=FilmResponse, summary="Get film by ID")
def get_film(film_id: int):
    result = film_handler.handle_get_film(film_id)
    return result.get("data", result)


@router.post("", summary="Create a new film")
def create_film(payload: FilmCreate) -> Dict[str, Any]:
    return film_handler.handle_create_film(payload.model_dump())


@router.patch("/{film_id}", summary="Update a film")
def update_film(film_id: int, payload: FilmUpdate) -> Dict[str, Any]:
    return film_handler.handle_update_film(film_id, payload.model_dump(exclude_unset=True))


@router.delete("/{film_id}", summary="Delete a film")
def delete_film(film_id: int) -> Dict[str, Any]:
    return film_handler.handle_delete_film(film_id)
