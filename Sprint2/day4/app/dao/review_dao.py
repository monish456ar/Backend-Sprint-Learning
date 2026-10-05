from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.review import Review


class ReviewDAO:
    """Review Data Access Object providing explicit SQLAlchemy 2.0 query constructs (select, insert, update, delete)."""

    @staticmethod
    async def get_reviews_for_film(db: AsyncSession, film_id: UUID) -> List[Review]:
        """READ: Retrieves all reviews for a specified film ordered by created_at."""
        stmt = select(Review).where(Review.film_id == film_id).order_by(Review.created_at)
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
