from typing import Any, Dict, List
from fastapi import APIRouter, status
from app.handlers import review_handler
from app.schemas.review_schemas import ReviewCreate, ReviewUpdate, ReviewResponse

router = APIRouter(tags=["Reviews"])


@router.get("/films/{film_id}/reviews", response_model=List[ReviewResponse], summary="Get all reviews for a film")
def get_film_reviews(film_id: int) -> List[ReviewResponse]:
    result = review_handler.handle_get_reviews_for_film(film_id)
    return result.get("data", [])


@router.post(
    "/films/{film_id}/reviews",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a review for a film",
)
def create_film_review(film_id: int, payload: ReviewCreate) -> ReviewResponse:
    # Ensure film_id from URL path matches or is passed into review creation
    review_data = payload.model_dump()
    review_data["film_id"] = film_id
    result = review_handler.handle_create_review_for_film(film_id, review_data)
    return result["data"]


@router.patch("/reviews/{review_id}", response_model=ReviewResponse, summary="Update a review")
def update_review(review_id: int, payload: ReviewUpdate) -> ReviewResponse:
    result = review_handler.handle_update_review(review_id, payload.model_dump(exclude_unset=True))
    return result["data"]


@router.delete("/reviews/{review_id}", summary="Delete a review")
def delete_review(review_id: int) -> Dict[str, Any]:
    return review_handler.handle_delete_review(review_id)
