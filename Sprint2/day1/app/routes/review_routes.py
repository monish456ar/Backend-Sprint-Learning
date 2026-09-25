from typing import Any, Dict
from fastapi import APIRouter
from app.handlers import review_handler
from app.schemas.review_schemas import ReviewCreate, ReviewUpdate

router = APIRouter(tags=["Reviews"])


@router.get("/films/{film_id}/reviews", summary="Get all reviews for a film")
def get_film_reviews(film_id: int) -> Dict[str, Any]:
    return review_handler.handle_get_reviews_for_film(film_id)


@router.post("/films/{film_id}/reviews", summary="Create a review for a film")
def create_film_review(film_id: int, payload: ReviewCreate) -> Dict[str, Any]:
    return review_handler.handle_create_review_for_film(film_id, payload.model_dump())


@router.patch("/reviews/{review_id}", summary="Update a review")
def update_review(review_id: int, payload: ReviewUpdate) -> Dict[str, Any]:
    return review_handler.handle_update_review(review_id, payload.model_dump(exclude_unset=True))


@router.delete("/reviews/{review_id}", summary="Delete a review")
def delete_review(review_id: int) -> Dict[str, Any]:
    return review_handler.handle_delete_review(review_id)
