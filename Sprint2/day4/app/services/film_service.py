import json
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.dao.film_dao import FilmDAO
from app.dao.review_dao import ReviewDAO
from app.database.redis_client import redis_client
from app.exceptions.domain_exceptions import (
    FilmAlreadyExistsError,
    FilmHasActiveReviewsError,
    FilmNotFoundError,
)
from app.models.film import Film

logger = logging.getLogger("film_service")


class FilmService:
    """Service layer managing film domain logic, business rules, DAO orchestration, and Redis caching."""

    @classmethod
    def _build_list_cache_key(
        cls,
        genre: Optional[str] = None,
        release_year: Optional[int] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
    ) -> str:
        """Constructs a deterministic Redis cache key for film list queries."""
        genre_part = (genre or "").strip().lower() or "*"
        rel_part = str(release_year) if release_year is not None else "*"
        start_part = str(start_year) if start_year is not None else "*"
        end_part = str(end_year) if end_year is not None else "*"
        return f"films:list:genre={genre_part}:year={rel_part}:start={start_part}:end={end_part}"

    @classmethod
    async def invalidate_film_cache(cls) -> None:
        """
        Invalidates all cached film list entries in Redis.
        Explicitly removes all keys matching 'films:list:*'.
        """
        try:
            keys: List[str] = []
            async for key in redis_client.scan_iter(match="films:list:*"):
                keys.append(key)
            if keys:
                await redis_client.delete(*keys)
                logger.info("Invalidated %d film list cache key(s) from Redis: %s", len(keys), keys)
        except Exception as e:
            logger.warning("Failed to invalidate film cache from Redis: %s", str(e))

    @classmethod
    async def list_films(
        cls,
        db: AsyncSession,
        genre: Optional[str] = None,
        release_year: Optional[int] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Read-through caching layer for listing films:
        1. Check Redis for cached serialized results.
        2. If HIT: return cached results directly without querying the database.
        3. If MISS: fetch from PostgreSQL, serialize, store in Redis with TTL, and return.
        """
        cache_key = cls._build_list_cache_key(
            genre=genre,
            release_year=release_year,
            start_year=start_year,
            end_year=end_year,
        )

        try:
            cached_data = await redis_client.get(cache_key)
            if cached_data is not None:
                logger.info("Redis cache HIT for '%s'", cache_key)
                return json.loads(cached_data)
        except Exception as e:
            logger.warning("Redis cache read error for '%s': %s", cache_key, str(e))

        logger.info("Redis cache MISS for '%s'. Querying database...", cache_key)
        films = await FilmDAO.list_films(
            db=db,
            genre=genre,
            release_year=release_year,
            start_year=start_year,
            end_year=end_year,
        )

        serialized_films = [
            {
                "id": str(film.id),
                "title": film.title,
                "release_year": film.release_year,
                "genre": film.genre,
                "director": film.director,
                "hero": film.hero,
                "is_deleted": film.is_deleted,
            }
            for film in films
        ]

        try:
            await redis_client.set(
                cache_key,
                json.dumps(serialized_films),
                ex=settings.film_cache_ttl_seconds,
            )
            logger.info(
                "Stored %d film(s) in Redis cache under '%s' with TTL %ds",
                len(serialized_films),
                cache_key,
                settings.film_cache_ttl_seconds,
            )
        except Exception as e:
            logger.warning("Redis cache write error for '%s': %s", cache_key, str(e))

        return serialized_films

    @classmethod
    async def retrieve_film(cls, db: AsyncSession, film_id: UUID) -> Film:
        """Retrieves a single film by ID. Raises FilmNotFoundError if not found."""
        logger.debug("Retrieving film %s", film_id)
        film = await FilmDAO.get_film_by_id(db, film_id)
        if film is None:
            logger.warning("Film %s not found", film_id)
            raise FilmNotFoundError(film_id)
        logger.info("Retrieved film %s successfully", film_id)
        return film

    @classmethod
    async def add_film(cls, db: AsyncSession, film_data: Dict[str, Any]) -> Film:
        """
        Creates a new film via FilmDAO and invalidates all film list caches in Redis.
        Business Rules:
        - Film with same title cannot be created twice (raises FilmAlreadyExistsError).
        """
        title = str(film_data.get("title", "")).strip()
        logger.debug("Starting film creation for '%s'", title)

        # Enforce business rule: Prevent duplicate films with the same title
        existing_film = await FilmDAO.get_film_by_title(db, title)
        if existing_film:
            logger.warning("Film title already exists: '%s'", title)
            raise FilmAlreadyExistsError(title)

        try:
            film = await FilmDAO.create_film(db, film_data)
            logger.info("Film '%s' created successfully with id %s", film.title, film.id)
            # Invalidate all film list caches upon creation
            await cls.invalidate_film_cache()
            return film
        except Exception as e:
            logger.error("Failed to save film because of database error: %s", str(e))
            raise

    @classmethod
    async def filter_films(
        cls, db: AsyncSession, start_year: int, end_year: int
    ) -> List[Dict[str, Any]]:
        """Filters films within a release year window with read-through caching."""
        logger.debug("Filtering films between years %d and %d", start_year, end_year)
        return await cls.list_films(db, start_year=start_year, end_year=end_year)

    @classmethod
    async def modify_film(
        cls, db: AsyncSession, film_id: UUID, film_data: Dict[str, Any]
    ) -> Film:
        """Updates film fields and invalidates all film list caches. Raises FilmNotFoundError if film does not exist."""
        logger.debug("Starting film update for id %s", film_id)
        updated_film = await FilmDAO.update_film(db, film_id, film_data)
        if updated_film is None:
            logger.warning("Film %s not found for update", film_id)
            raise FilmNotFoundError(film_id)

        # Invalidate all film list caches upon update
        await cls.invalidate_film_cache()
        logger.info("Film %s updated successfully and cache invalidated", film_id)
        return updated_film

    @classmethod
    async def soft_remove_film(cls, db: AsyncSession, film_id: UUID) -> bool:
        """
        Soft-deletes a film and invalidates all film list caches.
        Business Rules:
        - Film must exist (raises FilmNotFoundError if not).
        - Film cannot be soft-deleted while it has active reviews (raises FilmHasActiveReviewsError).
        """
        logger.debug("Initiating soft delete for film %s", film_id)
        film = await FilmDAO.get_film_by_id(db, film_id)
        if film is None:
            logger.warning("Film %s not found for soft delete", film_id)
            raise FilmNotFoundError(film_id)

        # Enforce business rule: A film cannot be soft-deleted while it has active reviews
        active_review_count = await ReviewDAO.count_reviews_for_film(db, film_id)
        if active_review_count > 0:
            logger.warning(
                "Film %s has %d active review(s), soft delete rejected",
                film_id,
                active_review_count,
            )
            raise FilmHasActiveReviewsError(
                film_id=film_id, active_review_count=active_review_count
            )

        success = await FilmDAO.soft_delete_film(db, film_id)
        if not success:
            logger.warning("Film %s soft delete failed", film_id)
            raise FilmNotFoundError(film_id)

        # Invalidate all film list caches upon soft-delete
        await cls.invalidate_film_cache()
        logger.info("Film %s soft-deleted successfully and cache invalidated", film_id)
        return True

    @classmethod
    async def remove_film(cls, db: AsyncSession, film_id: UUID) -> bool:
        """Hard-deletes a film and invalidates all film list caches. Raises FilmNotFoundError if film does not exist."""
        logger.debug("Initiating hard delete for film %s", film_id)
        film = await FilmDAO.get_film_by_id(db, film_id, include_deleted=True)
        if film is None:
            logger.warning("Film %s not found for hard delete", film_id)
            raise FilmNotFoundError(film_id)

        success = await FilmDAO.delete_film(db, film_id)
        if not success:
            logger.warning("Film %s hard delete failed", film_id)
            raise FilmNotFoundError(film_id)

        # Invalidate all film list caches upon hard delete
        await cls.invalidate_film_cache()
        logger.info("Film %s hard-deleted successfully and cache invalidated", film_id)
        return True


# Backward-compatible function aliases
list_films = FilmService.list_films
retrieve_film = FilmService.retrieve_film
add_film = FilmService.add_film
filter_films = FilmService.filter_films
modify_film = FilmService.modify_film
soft_remove_film = FilmService.soft_remove_film
remove_film = FilmService.remove_film
invalidate_film_cache = FilmService.invalidate_film_cache
