from typing import Any, Dict, List
from fastapi import APIRouter, Depends, status
from app.handlers import film_handler
from app.schemas.film_schemas import FilmCreate, FilmUpdate, FilmResponse, FilmFilterQuery
from app.dependencies import get_config, get_db, get_trace_id

router = APIRouter(prefix="/films", tags=["Films"])


@router.get("", summary="Get all films")
def get_films(
    config=Depends(get_config),
    db=Depends(get_db),
    trace_id=Depends(get_trace_id),
) -> Dict[str, Any]:
    return {
        "message": "Films",
        "api_version": config.api_version,
        "db": db,
        "trace_id": trace_id,
    }


@router.get("/{film_id}", summary="Get film by ID")
def get_film(
    film_id: int,
    config=Depends(get_config),
    db=Depends(get_db),
    trace_id=Depends(get_trace_id),
) -> Dict[str, Any]:
    return {
        "film_id": film_id,
        "api_version": config.api_version,
        "db": db,
        "trace_id": trace_id,
    }


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
