from typing import Any, Dict, List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import (
    get_config,
    get_db,
    get_trace_id,
    require_role,
)
from app.handlers import film_handler
from app.schemas.film_schemas import (
    FilmCreate,
    FilmFilterQuery,
    FilmResponse,
    FilmUpdate,
)

router = APIRouter(prefix="/films", tags=["Films"])


@router.get(
    "", response_model=List[FilmResponse], summary="Get all films with optional filters"
)
async def get_all_films(
    genre: Optional[str] = Query(None, description="Filter by genre"),
    release_year: Optional[int] = Query(None, description="Filter by exact release year"),
    start_year: Optional[int] = Query(None, description="Filter by minimum release year"),
    end_year: Optional[int] = Query(None, description="Filter by maximum release year"),
    db: AsyncSession = Depends(get_db),
    config=Depends(get_config),
    trace_id=Depends(get_trace_id),
) -> List[FilmResponse]:
    return await film_handler.handle_get_all_films(
        db=db,
        genre=genre,
        release_year=release_year,
        start_year=start_year,
        end_year=end_year,
    )


@router.get("/{film_id}", response_model=FilmResponse, summary="Get film by ID")
async def get_film(
    film_id: UUID,
    db: AsyncSession = Depends(get_db),
    config=Depends(get_config),
    trace_id=Depends(get_trace_id),
) -> FilmResponse:
    return await film_handler.handle_get_film(db, film_id)


@router.post(
    "",
    response_model=FilmResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new film (Admin only)",
    dependencies=[Depends(require_role("admin"))],
)
async def create_film(
    payload: FilmCreate,
    db: AsyncSession = Depends(get_db),
) -> FilmResponse:
    return await film_handler.handle_create_film(db, payload.model_dump())


@router.post(
    "/filter",
    response_model=List[FilmResponse],
    summary="Filter films by year range (Cross-field validation)",
)
async def filter_films(
    payload: FilmFilterQuery,
    db: AsyncSession = Depends(get_db),
) -> List[FilmResponse]:
    return await film_handler.handle_filter_films(db, payload.model_dump())


@router.patch(
    "/{film_id}",
    response_model=FilmResponse,
    summary="Update a film (Admin only)",
    dependencies=[Depends(require_role("admin"))],
)
async def update_film(
    film_id: UUID,
    payload: FilmUpdate,
    db: AsyncSession = Depends(get_db),
) -> FilmResponse:
    return await film_handler.handle_update_film(
        db, film_id, payload.model_dump(exclude_unset=True)
    )


@router.put(
    "/{film_id}",
    response_model=FilmResponse,
    summary="Update a film full (Admin only)",
    dependencies=[Depends(require_role("admin"))],
)
async def update_film_put(
    film_id: UUID,
    payload: FilmUpdate,
    db: AsyncSession = Depends(get_db),
) -> FilmResponse:
    return await film_handler.handle_update_film(
        db, film_id, payload.model_dump(exclude_unset=True)
    )


@router.delete(
    "/{film_id}/soft",
    summary="Soft-delete a film (Admin only)",
    dependencies=[Depends(require_role("admin"))],
)
async def soft_delete_film(
    film_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    return await film_handler.handle_soft_delete_film(db, film_id)


@router.delete(
    "/{film_id}",
    summary="Delete a film",
    dependencies=[Depends(require_role("admin"))],
)
async def delete_film(
    film_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    return await film_handler.handle_delete_film(db, film_id)
