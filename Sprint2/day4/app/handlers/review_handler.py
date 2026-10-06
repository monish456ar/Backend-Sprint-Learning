from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.review import Review
from app.services.review_service import ReviewService


async def handle_get_reviews_for_film(
    db: AsyncSession, film_id: UUID
) -> List[Review]:
    """Retrieves all reviews for a film. Domain exceptions bubble up to centralized handlers."""
    return await ReviewService.list_reviews_for_film(db, film_id)


async def handle_get_film_average_rating(
    db: AsyncSession, film_id: UUID
) -> Dict[str, Any]:
    """Retrieves average rating for a film. Domain exceptions bubble up to centralized handlers."""
    avg_rating = await ReviewService.get_film_average_rating(db, film_id)
    return {
        "film_id": str(film_id),
        "average_rating": avg_rating,
    }


async def handle_create_review_for_film(
    db: AsyncSession,
    film_id: UUID,
    review_data: Dict[str, Any],
) -> Review:
    """Creates a review for a film. Business rule exceptions bubble up to centralized handlers."""
    return await ReviewService.add_review_for_film(db, film_id, review_data)


async def handle_update_review(
    db: AsyncSession,
    review_id: UUID,
    review_data: Dict[str, Any],
    current_user_id: Optional[UUID] = None,
) -> Review:
    """Updates a review. Ownership and not-found exceptions bubble up to centralized handlers."""
    return await ReviewService.modify_review(
        db=db,
        review_id=review_id,
        review_data=review_data,
        current_user_id=current_user_id,
    )


async def handle_delete_review(
    db: AsyncSession,
    review_id: UUID,
    current_user_id: Optional[UUID] = None,
) -> Dict[str, Any]:
    """Deletes a review. Domain exceptions bubble up to centralized handlers."""
    await ReviewService.remove_review(db, review_id, current_user_id=current_user_id)
    return {"message": f"Review {review_id} deleted successfully", "review_id": str(review_id)}

