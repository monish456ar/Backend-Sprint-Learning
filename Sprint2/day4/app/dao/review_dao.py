from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.models.review import Review


class ReviewDAO:
    """Review Data Access Object providing explicit SQLAlchemy 2.0 query constructs (select, insert, update, delete)."""

    @staticmethod
    async def get_reviews_for_film_paginated(
        db: AsyncSession,
        film_id: UUID,
        page: int = 1,
        page_size: int = 10,
        min_rating: Optional[int] = None,
        max_rating: Optional[int] = None,
    ) -> Tuple[List[Review], int]:
        """
        READ: Retrieves paginated reviews for a film using SQL LIMIT/OFFSET.
        Uses joinedload(Review.user) to eliminate the N+1 query problem when accessing reviewer details.
        """
        # Base filter condition
        base_stmt = select(Review).where(Review.film_id == film_id)
        if min_rating is not None:
            base_stmt = base_stmt.where(Review.rating >= min_rating)
        if max_rating is not None:
            base_stmt = base_stmt.where(Review.rating <= max_rating)

        # 1. Total matching reviews count
        count_stmt = select(func.count(Review.id)).where(Review.film_id == film_id)
        if min_rating is not None:
            count_stmt = count_stmt.where(Review.rating >= min_rating)
        if max_rating is not None:
            count_stmt = count_stmt.where(Review.rating <= max_rating)

        total_res = await db.execute(count_stmt)
        total: int = total_res.scalar_one() or 0

        # 2. Paginated rows with joinedload eager-loading to prevent N+1 queries
        offset = max(0, (page - 1) * page_size)
        query_stmt = (
            base_stmt
            .options(joinedload(Review.user))
            .order_by(Review.created_at.desc(), Review.id.desc())
            .offset(offset)
            .limit(page_size)
        )
        result = await db.execute(query_stmt)
        reviews = list(result.scalars().all())
        return reviews, total

    @staticmethod
    async def get_reviews_for_film(db: AsyncSession, film_id: UUID) -> List[Review]:
        """READ: Retrieves all reviews for a specified film ordered by created_at."""
        stmt = (
            select(Review)
            .where(Review.film_id == film_id)
            .options(joinedload(Review.user))
            .order_by(Review.created_at)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())


    @staticmethod
    async def get_review_by_id(db: AsyncSession, review_id: UUID) -> Optional[Review]:
        """READ: Retrieves a single review by its primary key ID using scalar_one_or_none()."""
        stmt = select(Review).where(Review.id == review_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_review(
        db: AsyncSession, user_id: UUID, film_id: UUID
    ) -> Optional[Review]:
        """READ: Retrieves a review by a specific user for a specific film if one exists."""
        stmt = (
            select(Review)
            .where(Review.user_id == user_id, Review.film_id == film_id)
            .limit(1)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_user_review_for_film(
        db: AsyncSession, user_id: UUID, film_id: UUID
    ) -> Optional[Review]:
        """Alias for get_user_review."""
        return await ReviewDAO.get_user_review(db, user_id, film_id)

    @staticmethod
    async def count_reviews_for_film(db: AsyncSession, film_id: UUID) -> int:
        """READ: Counts active reviews associated with a specific film."""
        stmt = select(func.count(Review.id)).where(Review.film_id == film_id)
        result = await db.execute(stmt)
        return result.scalar_one() or 0

    @staticmethod
    async def get_average_rating_for_film(
        db: AsyncSession, film_id: UUID
    ) -> Optional[float]:
        """READ (Aggregate): Calculates average rating using SQL func.avg()."""
        stmt = select(func.avg(Review.rating)).where(Review.film_id == film_id)
        result = await db.execute(stmt)
        avg_rating = result.scalar_one_or_none()
        return round(float(avg_rating), 2) if avg_rating is not None else None

    @staticmethod
    async def get_average_ratings_for_films(
        db: AsyncSession, film_ids: List[UUID]
    ) -> Dict[UUID, Optional[float]]:
        """
        READ (Batch Aggregate): Calculates average ratings for multiple films in a single SQL query.
        Eliminates the N+1 query problem when listing films with ratings.
        """
        if not film_ids:
            return {}
        stmt = (
            select(Review.film_id, func.avg(Review.rating))
            .where(Review.film_id.in_(film_ids))
            .group_by(Review.film_id)
        )
        result = await db.execute(stmt)
        rows = result.all()
        mapping: Dict[UUID, Optional[float]] = {f_id: None for f_id in film_ids}
        for f_id, avg_val in rows:
            if avg_val is not None:
                mapping[f_id] = round(float(avg_val), 2)
        return mapping


    @staticmethod
    async def create_review(
        db: AsyncSession,
        film_id: UUID,
        user_id: UUID,
        rating: int,
        review_body: str,
    ) -> Review:
        """CREATE: Inserts a review, commits, and refreshes the entity with user loaded."""
        review = Review(
            film_id=film_id,
            user_id=user_id,
            rating=rating,
            review_body=review_body,
        )
        db.add(review)
        await db.commit()
        await db.refresh(review, ["user"])
        return review

    @staticmethod
    async def update_review(
        db: AsyncSession,
        review_id: UUID,
        review_data: Dict[str, Any],
    ) -> Optional[Review]:
        """UPDATE: Updates review fields and uses db.refresh(review, ['user'])."""
        review = await ReviewDAO.get_review_by_id(db, review_id)
        if not review:
            return None

        for key, value in review_data.items():
            if value is not None and hasattr(review, key):
                setattr(review, key, value)

        await db.commit()
        await db.refresh(review, ["user"])
        return review

    @staticmethod
    async def delete_review(db: AsyncSession, review_id: UUID) -> bool:
        """DELETE: Deletes a review using an explicit SQLAlchemy 2.0 delete() statement."""
        stmt = delete(Review).where(Review.id == review_id)
        result = await db.execute(stmt)
        await db.commit()
        return bool(result.rowcount and result.rowcount > 0)
