from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.film import Film
from app.services.film_service import FilmService


async def handle_get_all_films(
    db: AsyncSession,
    genre: Optional[str] = None,
    release_year: Optional[int] = None,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
) -> List[Film]:
    """Handles listing films with optional query filters."""
    return await FilmService.list_films(
        db=db,
        genre=genre,
        release_year=release_year,
        start_year=start_year,
        end_year=end_year,
    )


async def handle_get_film(db: AsyncSession, film_id: UUID) -> Film:
    """Handles retrieving a film by ID. Domain exceptions bubble up to centralized handlers."""
    return await FilmService.retrieve_film(db, film_id)


async def handle_create_film(
    db: AsyncSession, film_data: Dict[str, Any]
) -> Film:
    """Handles creating a new film."""
    return await FilmService.add_film(db, film_data)


async def handle_filter_films(
    db: AsyncSession, filter_data: Dict[str, Any]
) -> List[Film]:
    """Handles filtering films by year range."""
    start_year = filter_data.get("start_year", 0)
    end_year = filter_data.get("end_year", 9999)
    return await FilmService.filter_films(db, start_year, end_year)


async def handle_update_film(
    db: AsyncSession, film_id: UUID, film_data: Dict[str, Any]
) -> Film:
    """Handles updating film fields. Domain exceptions bubble up to centralized handlers."""
    return await FilmService.modify_film(db, film_id, film_data)


async def handle_soft_delete_film(
    db: AsyncSession, film_id: UUID
) -> Dict[str, Any]:
    """Handles soft-deleting a film by ID. Enforces active reviews rule via FilmService."""
    await FilmService.soft_remove_film(db, film_id)
    return {
        "message": f"Film {film_id} soft-deleted successfully",
        "film_id": str(film_id),
        "status": "archived",
    }


async def handle_delete_film(db: AsyncSession, film_id: UUID) -> Dict[str, Any]:
    """Handles hard-deleting a film by ID. Domain exceptions bubble up to centralized handlers."""
    await FilmService.remove_film(db, film_id)
    return {"message": f"Film {film_id} deleted successfully", "film_id": str(film_id)}
