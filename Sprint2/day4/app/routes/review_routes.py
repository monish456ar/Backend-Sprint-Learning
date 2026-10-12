from typing import Any, Dict, List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import (
    get_config,
    get_db,
    require_role,
    Settings,
)
from app.handlers import review_handler
from app.models.user import User
from app.schemas.pagination_schemas import PaginatedResponse
from app.schemas.review_schemas import ReviewCreate, ReviewResponse, ReviewUpdate

router = APIRouter(tags=["Reviews"])


@router.get(
    "/films/{film_id}/reviews",
    response_model=PaginatedResponse[ReviewResponse],
    summary="Get paginated reviews for a film (Public)",
)
async def get_film_reviews(
    film_id: UUID,
    page: int = Query(1, ge=1, description="Current page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Records requested per page"),
    min_rating: Optional[int] = Query(None, ge=1, le=10, description="Filter rating >= min_rating"),
    max_rating: Optional[int] = Query(None, ge=1, le=10, description="Filter rating <= max_rating"),
    db: AsyncSession = Depends(get_db),
    config: Settings = Depends(get_config),
) -> PaginatedResponse[ReviewResponse]:
    """Retrieves paginated reviews for a specific film with eager loading of reviewer."""
    if min_rating is not None and max_rating is not None and min_rating > max_rating:
        raise ValueError("min_rating must be less than or equal to max_rating")

    return await review_handler.handle_get_reviews_for_film_paginated(
        db=db,
        film_id=film_id,
        page=page,
        page_size=page_size,
        min_rating=min_rating,
        max_rating=max_rating,
    )



@router.get(
    "/films/{film_id}/average-rating",
    summary="Get average rating for a film (Public)",
)
async def get_film_average_rating(
    film_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    return await review_handler.handle_get_film_average_rating(db, film_id)


@router.post(
    "/films/{film_id}/reviews",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a review for a film (Admin & Critic)",
)
async def create_film_review(
    film_id: UUID,
    payload: ReviewCreate,
    current_user: User = Depends(require_role("admin", "critic")),
    db: AsyncSession = Depends(get_db),
) -> ReviewResponse:
    review_data = payload.model_dump(exclude_unset=True)
    review_data["user_id"] = current_user.id
    return await review_handler.handle_create_review_for_film(db, film_id, review_data)


@router.patch(
    "/reviews/{review_id}",
    response_model=ReviewResponse,
    summary="Update a review (Critic owner or Admin)",
)
async def update_review(
    review_id: UUID,
    payload: ReviewUpdate,
    current_user: User = Depends(require_role("admin", "critic")),
    db: AsyncSession = Depends(get_db),
) -> ReviewResponse:
    review_data = payload.model_dump(exclude_unset=True)
    return await review_handler.handle_update_review(
        db=db,
        review_id=review_id,
        review_data=review_data,
        current_user_id=current_user.id,
        current_user_role=current_user.role,
    )


@router.delete(
    "/reviews/{review_id}",
    summary="Delete a review (Critic owner or Admin)",
)
async def delete_review(
    review_id: UUID,
    current_user: User = Depends(require_role("admin", "critic")),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    return await review_handler.handle_delete_review(
        db=db,
        review_id=review_id,
        current_user_id=current_user.id,
        current_user_role=current_user.role,
    )


