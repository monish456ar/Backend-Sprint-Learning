import logging
from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.film_dao import FilmDAO
from app.dao.review_dao import ReviewDAO
from app.exceptions.domain_exceptions import (
    FilmAlreadyExistsError,
    FilmHasActiveReviewsError,
    FilmNotFoundError,
)
from app.models.film import Film

logger = logging.getLogger("film_service")


class FilmService:
    """Service layer managing film domain logic, business rules, and DAO orchestration."""

    @classmethod
    async def list_films(
        cls,
        db: AsyncSession,
        genre: Optional[str] = None,
        release_year: Optional[int] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
    ) -> List[Film]:
        """Retrieves a list of films using FilmDAO with optional filters."""
        logger.debug(
            "Listing films: genre=%s, release_year=%s, start_year=%s, end_year=%s",
            genre,
            release_year,
            start_year,
            end_year,
        )
        films = await FilmDAO.list_films(
            db=db,
            genre=genre,
            release_year=release_year,
            start_year=start_year,
            end_year=end_year,
        )
        logger.info("Found %d film(s)", len(films))
        return films

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
        Creates a new film via FilmDAO.
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
            return film
        except Exception as e:
            logger.error("Failed to save film because of database error: %s", str(e))
            raise

    @classmethod
    async def filter_films(
        cls, db: AsyncSession, start_year: int, end_year: int
    ) -> List[Film]:
        """Filters films within a release year window."""
        logger.debug("Filtering films between years %d and %d", start_year, end_year)
        films = await FilmDAO.list_films(db, start_year=start_year, end_year=end_year)
        logger.info("Filtered %d film(s)", len(films))
        return films

    @classmethod
    async def modify_film(
        cls, db: AsyncSession, film_id: UUID, film_data: Dict[str, Any]
    ) -> Film:
        """Updates film fields. Raises FilmNotFoundError if film does not exist."""
        logger.debug("Starting film update for id %s", film_id)
        updated_film = await FilmDAO.update_film(db, film_id, film_data)
        if updated_film is None:
            logger.warning("Film %s not found for update", film_id)
            raise FilmNotFoundError(film_id)
        logger.info("Film %s updated successfully", film_id)
        return updated_film

    @classmethod
    async def soft_remove_film(cls, db: AsyncSession, film_id: UUID) -> bool:
        """
        Soft-deletes a film.
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

        logger.info("Film %s soft-deleted successfully", film_id)
        return True

    @classmethod
    async def remove_film(cls, db: AsyncSession, film_id: UUID) -> bool:
        """Hard-deletes a film. Raises FilmNotFoundError if film does not exist."""
        logger.debug("Initiating hard delete for film %s", film_id)
        film = await FilmDAO.get_film_by_id(db, film_id, include_deleted=True)
        if film is None:
            logger.warning("Film %s not found for hard delete", film_id)
            raise FilmNotFoundError(film_id)

        success = await FilmDAO.delete_film(db, film_id)
        if not success:
            logger.warning("Film %s hard delete failed", film_id)
            raise FilmNotFoundError(film_id)

        logger.info("Film %s hard-deleted successfully", film_id)
        return True


# Backward-compatible function aliases
list_films = FilmService.list_films
retrieve_film = FilmService.retrieve_film
add_film = FilmService.add_film
filter_films = FilmService.filter_films
modify_film = FilmService.modify_film
soft_remove_film = FilmService.soft_remove_film
remove_film = FilmService.remove_film
