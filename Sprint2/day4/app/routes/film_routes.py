from typing import Any, Dict, List, Optional, Union
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
from app.schemas.pagination_schemas import (
    CursorPaginatedResponse,
    FilmFilterParams,
    PaginatedResponse,
)

router = APIRouter(prefix="/films", tags=["Films"])


@router.get(
    "/cursor",
    response_model=CursorPaginatedResponse[FilmResponse],
    summary="Get films using cursor-based pagination",
)
async def get_films_cursor(
    filters: FilmFilterParams = Depends(),
    cursor: Optional[str] = Query(None, description="Opaque cursor token representing the next batch position"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to fetch"),
    db: AsyncSession = Depends(get_db),
) -> CursorPaginatedResponse[FilmResponse]:
    """Dedicated cursor-based pagination endpoint with multi-field filtering."""
    return await film_handler.handle_get_all_films_cursor(
        db=db,
        cursor=cursor,
        limit=limit,
        genre=filters.genre,
        from_year=filters.from_year,
        to_year=filters.to_year,
        director=filters.director,
    )


@router.get(
    "",
    response_model=Union[PaginatedResponse[FilmResponse], CursorPaginatedResponse[FilmResponse]],
    summary="Get films with offset pagination (default) or cursor pagination",
)
async def get_all_films(
    filters: FilmFilterParams = Depends(),
    page: int = Query(1, ge=1, description="Current page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Records requested per page"),
    cursor: Optional[str] = Query(None, description="Optional cursor for cursor-based pagination mode"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Batch limit if using cursor mode"),
    db: AsyncSession = Depends(get_db),
    config=Depends(get_config),
    trace_id=Depends(get_trace_id),
) -> Any:
    """
    Retrieves films using either offset-based pagination (default) or cursor-based pagination.
    Supports multi-field filtering:
    - genre: Exact match (case-insensitive)
    - from_year / to_year: Release year range
    - director: Case-insensitive substring search
    """
    if cursor is not None:
        return await film_handler.handle_get_all_films_cursor(
            db=db,
            cursor=cursor,
            limit=limit or page_size,
            genre=filters.genre,
            from_year=filters.from_year,
            to_year=filters.to_year,
            director=filters.director,
        )

    return await film_handler.handle_get_all_films_paginated(
        db=db,
        genre=filters.genre,
        from_year=filters.from_year,
        to_year=filters.to_year,
        director=filters.director,
        page=page,
        page_size=page_size,
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
