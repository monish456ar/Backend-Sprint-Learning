import logging
from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.film_dao import FilmDAO
from app.dao.review_dao import ReviewDAO
from app.dao.user_dao import UserDAO
from app.exceptions.domain_exceptions import (
    FilmNotFoundError,
    ReviewAlreadyExistsError,
    ReviewNotFoundError,
    ReviewNotOwnerError,
    UserNotFoundError,
)
from app.models.review import Review

logger = logging.getLogger("review_service")


class ReviewService:
    """Service layer managing review domain logic, business rules, and DAO orchestration."""

    @classmethod
    async def list_reviews_for_film(
        cls, db: AsyncSession, film_id: UUID
    ) -> List[Review]:
        """Lists reviews for a film. Verifies film exists first."""
        logger.debug("Listing reviews for film %s", film_id)
        film = await FilmDAO.get_film_by_id(db, film_id)
        if film is None:
            logger.warning("Film %s not found", film_id)
            raise FilmNotFoundError(film_id)
        reviews = await ReviewDAO.get_reviews_for_film(db, film_id)
        logger.info("Found %d review(s) for film %s", len(reviews), film_id)
        return reviews

    @classmethod
    async def get_film_average_rating(
        cls, db: AsyncSession, film_id: UUID
    ) -> Optional[float]:
        """Calculates average rating for a film. Verifies film exists first."""
        logger.debug("Calculating average rating for film %s", film_id)
        film = await FilmDAO.get_film_by_id(db, film_id)
        if film is None:
            logger.warning("Film %s not found", film_id)
            raise FilmNotFoundError(film_id)
        avg = await ReviewDAO.get_average_rating_for_film(db, film_id)
        logger.info("Average rating for film %s is %s", film_id, avg)
        return avg

    @classmethod
    async def add_review_for_film(
        cls,
        db: AsyncSession,
        film_id: UUID,
        review_data: Dict[str, Any],
    ) -> Review:
        """
        Creates a review for a film.
        Business Rules:
        - Film must exist (raises FilmNotFoundError if not).
        - User must exist (raises UserNotFoundError if not).
        - A user cannot submit more than one review for the same film (raises ReviewAlreadyExistsError).
        """
        logger.debug("Starting review creation for film %s", film_id)

        # 1. Validate film
        film = await FilmDAO.get_film_by_id(db, film_id)
        if film is None:
            logger.warning("Film %s not found for review creation", film_id)
            raise FilmNotFoundError(film_id)

        # 2. Resolve user
        user_id = review_data.get("user_id")
        if user_id:
            if isinstance(user_id, str):
                user_id = UUID(user_id)
            user = await UserDAO.get_user_by_id(db, user_id)
            if user is None:
                logger.warning("User %s not found", user_id)
                raise UserNotFoundError(str(user_id))
        else:
            user = await UserDAO.get_current_user(db)
            if not user:
                user = await UserDAO.create_user(
                    db,
                    {
                        "username": "monish",
                        "email": "monish@filmreview.com",
                        "password": "secret_password",
                        "role": "user",
                    },
                )
            user_id = user.id

        # 3. Enforce business rule: A user cannot submit more than one review for the same film
        existing_review = await ReviewDAO.get_user_review(
            db, user_id=user_id, film_id=film_id
        )
        if existing_review:
            logger.warning(
                "User %s has already reviewed film %s (review id: %s)",
                user_id,
                film_id,
                existing_review.id,
            )
            raise ReviewAlreadyExistsError(user_id=user_id, film_id=film_id)

        # 4. Create and persist review via DAO
        review = await ReviewDAO.create_review(
            db=db,
            film_id=film_id,
            user_id=user_id,
            rating=review_data["rating"],
            review_body=review_data["review_body"],
        )
        logger.info(
            "Review created successfully with id %s for film %s by user %s",
            review.id,
            film_id,
            user_id,
        )
        return review

    @classmethod
    async def modify_review(
        cls,
        db: AsyncSession,
        review_id: UUID,
        review_data: Dict[str, Any],
        current_user_id: Optional[UUID] = None,
    ) -> Review:
        """
        Updates review rating and/or review_body.
        Business Rules:
        - Review must exist (raises ReviewNotFoundError if not).
        - Only the user who created a review can update its rating or body (raises ReviewNotOwnerError).
        """
        logger.debug("Starting review update for id %s", review_id)

        # 1. Retrieve existing review
        review = await ReviewDAO.get_review_by_id(db, review_id)
        if review is None:
            logger.warning("Review %s not found", review_id)
            raise ReviewNotFoundError(review_id)

        # 2. Determine acting user
        acting_user_id = current_user_id or review_data.get("user_id")
        if acting_user_id is None:
            curr_user = await UserDAO.get_current_user(db)
            acting_user_id = curr_user.id if curr_user else None
        elif isinstance(acting_user_id, str):
            acting_user_id = UUID(acting_user_id)

        # 3. Enforce ownership business rule
        if acting_user_id and review.user_id != acting_user_id:
            logger.warning(
                "User %s is not owner of review %s (owner: %s)",
                acting_user_id,
                review_id,
                review.user_id,
            )
            raise ReviewNotOwnerError(review_id=review_id, user_id=acting_user_id)

        # 4. Update review fields
        clean_update: Dict[str, Any] = {}
        if "rating" in review_data and review_data["rating"] is not None:
            clean_update["rating"] = review_data["rating"]
        if "review_body" in review_data and review_data["review_body"] is not None:
            clean_update["review_body"] = review_data["review_body"]

        updated_review = await ReviewDAO.update_review(db, review_id, clean_update)
        logger.info("Review %s updated successfully by user %s", review_id, acting_user_id)
        return updated_review

    @classmethod
    async def remove_review(cls, db: AsyncSession, review_id: UUID) -> bool:
        """Deletes review. Raises ReviewNotFoundError if review does not exist."""
        logger.debug("Starting review deletion for id %s", review_id)
        review = await ReviewDAO.get_review_by_id(db, review_id)
        if review is None:
            logger.warning("Review %s not found for deletion", review_id)
            raise ReviewNotFoundError(review_id)

        deleted = await ReviewDAO.delete_review(db, review_id)
        if not deleted:
            logger.warning("Review %s delete failed", review_id)
            raise ReviewNotFoundError(review_id)

        logger.info("Review %s deleted successfully", review_id)
        return True


# Backward-compatible function aliases
list_reviews_for_film = ReviewService.list_reviews_for_film
get_film_average_rating = ReviewService.get_film_average_rating
add_review_for_film = ReviewService.add_review_for_film
modify_review = ReviewService.modify_review
remove_review = ReviewService.remove_review
