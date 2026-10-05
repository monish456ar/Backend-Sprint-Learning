from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.film import Film


class FilmDAO:
    """Film Data Access Object providing explicit SQLAlchemy 2.0 query constructs (select, insert, update, delete)."""

    @staticmethod
    async def get_film_by_id(
        db: AsyncSession, film_id: UUID, include_deleted: bool = False
    ) -> Optional[Film]:
        """READ: Retrieves a single film by ID using explicit select()."""
        stmt = select(Film).where(Film.id == film_id)
        if not include_deleted:
            stmt = stmt.where(Film.is_deleted == False)  # noqa: E712
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_film_by_title(
        db: AsyncSession, title: str, include_deleted: bool = False
    ) -> Optional[Film]:
        """READ: Retrieves a single film by title (case-insensitive) using explicit select()."""
        stmt = select(Film).where(func.lower(Film.title) == title.strip().lower())
        if not include_deleted:
            stmt = stmt.where(Film.is_deleted == False)  
        stmt = stmt.limit(1)
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def list_films(
        db: AsyncSession,
        genre: Optional[str] = None,
        release_year: Optional[int] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
    ) -> List[Film]:
        """READ: Lists films with optional filtering using explicit select()."""
        stmt = select(Film).order_by(Film.id)
        if genre:
            stmt = stmt.where(Film.genre.ilike(f"%{genre}%"))
        if release_year is not None:
            stmt = stmt.where(Film.release_year == release_year)
        if start_year is not None:
            stmt = stmt.where(Film.release_year >= start_year)
        if end_year is not None:
            stmt = stmt.where(Film.release_year <= end_year)

        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def create_film(db: AsyncSession, film_data: Dict[str, Any]) -> Film:
        """CREATE: Inserts a new film into PostgreSQL."""
        film = Film(
            title=film_data["title"],
            release_year=film_data["release_year"],
            genre=film_data.get("genre", "Drama"),
            director=film_data.get("director", "Unknown"),
            hero=film_data.get("hero", "Unknown"),
            is_deleted=False,
        )
        db.add(film)
        await db.commit()
        await db.refresh(film)
        return film

    @staticmethod
    async def update_film(
        db: AsyncSession, film_id: UUID, film_data: Dict[str, Any]
    ) -> Optional[Film]:
        """UPDATE: Updates specified fields on a film and refreshes the entity."""
        film = await FilmDAO.get_film_by_id(db, film_id, include_deleted=True)
        if not film:
            return None
        for key, value in film_data.items():
            if value is not None and hasattr(film, key):
                setattr(film, key, value)
        await db.commit()
        await db.refresh(film)
        return film

    @staticmethod
    async def soft_delete_film(db: AsyncSession, film_id: UUID) -> bool:
        """UPDATE (Soft Delete): Sets is_deleted=True using an explicit SQLAlchemy 2.0 update() statement."""
        stmt = (
            update(Film)
            .where(Film.id == film_id, Film.is_deleted == False)
            .values(is_deleted=True)
        )
        result = await db.execute(stmt)
        await db.commit()
        return bool(result.rowcount and result.rowcount > 0)

    @staticmethod
    async def delete_film(db: AsyncSession, film_id: UUID) -> bool:
        """DELETE: Hard-deletes a film record using an explicit SQLAlchemy 2.0 delete() statement."""
        stmt = delete(Film).where(Film.id == film_id)
        result = await db.execute(stmt)
        await db.commit()
        return bool(result.rowcount and result.rowcount > 0)
