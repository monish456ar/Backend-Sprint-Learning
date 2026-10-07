from typing import Any, Dict, Optional
from uuid import UUID
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.film import Film
from app.models.review import Review
from app.models.user import User


class UserDAO:
    """User Data Access Object providing explicit SQLAlchemy 2.0 query constructs (select, insert, update, delete)."""

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """READ: Finds a user by email using explicit select() and scalar_one_or_none()."""
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
        """READ: Finds a user by ID using explicit select() and scalar_one_or_none()."""
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """READ: Finds a user by username using explicit select() and scalar_one_or_none()."""
        stmt = select(User).where(User.username == username)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(db: AsyncSession, user_data: Dict[str, Any]) -> User:
        """CREATE: Inserts a new user record into PostgreSQL."""
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data.get("password", "secret123"),
            role=user_data.get("role", "user"),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def update_user(
        db: AsyncSession, user_id: UUID, user_data: Dict[str, Any]
    ) -> Optional[User]:
        """UPDATE: Updates user fields and refreshes the entity."""
        user = await UserDAO.get_user_by_id(db, user_id)
        if not user:
            return None
        for key, value in user_data.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: UUID) -> bool:
        """DELETE: Deletes a user using an explicit SQLAlchemy 2.0 delete() statement."""
        stmt = delete(User).where(User.id == user_id)
        result = await db.execute(stmt)
        await db.commit()
        return bool(result.rowcount and result.rowcount > 0)

    @staticmethod
    async def authenticate_user(
        db: AsyncSession, credentials: Dict[str, Any]
    ) -> Optional[User]:
        """Authenticates user credentials by finding user and verifying password."""
        from app.dependencies.security import verify_password

        username = credentials.get("username")
        password = credentials.get("password")
        if not username or not password:
            return None

        user = await UserDAO.get_user_by_username(db, username)
        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return user


    @staticmethod
    async def get_current_user(
        db: AsyncSession, username: str = "monish"
    ) -> Optional[User]:
        """Retrieves current user record from PostgreSQL."""
        user = await UserDAO.get_user_by_username(db, username)
        if not user:
            result_any = await db.execute(select(User).limit(1))
            user = result_any.scalar_one_or_none()
        return user

    @staticmethod
    async def get_admin_stats(db: AsyncSession) -> Dict[str, Any]:
        """Calculates live platform counts using SQL aggregate queries."""
        user_count = await db.scalar(select(func.count(User.id))) or 0
        film_count = await db.scalar(select(func.count(Film.id))) or 0
        review_count = await db.scalar(select(func.count(Review.id))) or 0

        avg_rating_result = await db.scalar(select(func.avg(Review.rating)))
        overall_average_rating = round(float(avg_rating_result), 2) if avg_rating_result is not None else 0.0

        top_reviewer_stmt = (
            select(User.username)
            .join(Review, User.id == Review.user_id)
            .group_by(User.id, User.username)
            .order_by(func.count(Review.id).desc())
            .limit(1)
        )
        top_reviewer = await db.scalar(top_reviewer_stmt)

        return {
            "total_films": film_count,
            "total_reviews": review_count,
            "total_users": user_count,
            "overall_average_rating": overall_average_rating,
            "top_reviewer": top_reviewer or "None",
            "source": "postgresql",
        }

