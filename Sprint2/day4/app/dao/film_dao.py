from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID
from sqlalchemy import and_, delete, func, insert, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.security import decode_film_cursor, encode_film_cursor
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
    def _apply_film_filters(
        stmt,
        genre: Optional[str] = None,
        from_year: Optional[int] = None,
        to_year: Optional[int] = None,
        director: Optional[str] = None,
    ):
        """Applies independent, combinable multi-field filters to a Film select statement."""
        if genre and genre.strip():
            # Exact genre match (case-insensitive)
            stmt = stmt.where(func.lower(Film.genre) == genre.strip().lower())
        if from_year is not None:
            stmt = stmt.where(Film.release_year >= from_year)
        if to_year is not None:
            stmt = stmt.where(Film.release_year <= to_year)
        if director and director.strip():
            # Case-insensitive substring match
            stmt = stmt.where(Film.director.ilike(f"%{director.strip()}%"))
        return stmt

    @classmethod
    async def list_films_paginated(
        cls,
        db: AsyncSession,
        genre: Optional[str] = None,
        from_year: Optional[int] = None,
        to_year: Optional[int] = None,
        director: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[List[Film], int]:
        """
        READ: Retrieves an offset-paginated page of films with database filtering and counting.
        """
        # 1. Total matching count query in database
        count_stmt = select(func.count(Film.id)).where(Film.is_deleted == False)
        count_stmt = cls._apply_film_filters(
            count_stmt,
            genre=genre,
            from_year=from_year,
            to_year=to_year,
            director=director,
        )
        total_res = await db.execute(count_stmt)
        total: int = total_res.scalar_one() or 0

        # 2. Paginated rows query with stable ordering
        data_stmt = select(Film).where(Film.is_deleted == False)
        data_stmt = cls._apply_film_filters(
            data_stmt,
            genre=genre,
            from_year=from_year,
            to_year=to_year,
            director=director,
        )
        offset = max(0, (page - 1) * page_size)
        data_stmt = data_stmt.order_by(Film.created_at.desc(), Film.id.desc()).offset(offset).limit(page_size)

        result = await db.execute(data_stmt)
        films = list(result.scalars().all())
        return films, total

    @classmethod
    async def list_films_cursor(
        cls,
        db: AsyncSession,
        cursor: Optional[str] = None,
        limit: int = 10,
        genre: Optional[str] = None,
        from_year: Optional[int] = None,
        to_year: Optional[int] = None,
        director: Optional[str] = None,
    ) -> Tuple[List[Film], Optional[str]]:
        """
        READ: Cursor-based pagination on films.
        Fetches limit + 1 rows to determine if next batch exists.
        """
        stmt = select(Film).where(Film.is_deleted == False)
        stmt = cls._apply_film_filters(
            stmt,
            genre=genre,
            from_year=from_year,
            to_year=to_year,
            director=director,
        )

        if cursor:
            cursor_dt, cursor_id = decode_film_cursor(cursor)
            stmt = stmt.where(
                or_(
                    Film.created_at < cursor_dt,
                    and_(Film.created_at == cursor_dt, Film.id < cursor_id),
                )
            )

        stmt = stmt.order_by(Film.created_at.desc(), Film.id.desc()).limit(limit + 1)
        result = await db.execute(stmt)
        records = list(result.scalars().all())

        has_next = len(records) > limit
        items = records[:limit]

        next_cursor: Optional[str] = None
        if has_next and items:
            last_item = items[-1]
            next_cursor = encode_film_cursor(last_item.created_at, last_item.id)

        return items, next_cursor

    @classmethod
    async def list_films(
        cls,
        db: AsyncSession,
        genre: Optional[str] = None,
        release_year: Optional[int] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        from_year: Optional[int] = None,
        to_year: Optional[int] = None,
        director: Optional[str] = None,
    ) -> List[Film]:
        """READ: Backward-compatible film list without pagination envelope."""
        eff_from = from_year if from_year is not None else (release_year or start_year)
        eff_to = to_year if to_year is not None else (release_year or end_year)
        films, _ = await cls.list_films_paginated(
            db=db,
            genre=genre,
            from_year=eff_from,
            to_year=eff_to,
            director=director,
            page=1,
            page_size=1000,
        )
        return films


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

    @staticmethod
    async def search_films(db: AsyncSession, search_term: Optional[str] = None) -> List[Film]:
        """READ: Searches active films matching search_term in title or genre."""
        stmt = select(Film).where(Film.is_deleted == False)  
        if search_term and search_term.strip():
            pattern = f"%{search_term.strip()}%"
            stmt = stmt.where(Film.title.ilike(pattern) | Film.genre.ilike(pattern))
        stmt = stmt.order_by(Film.title)
        result = await db.execute(stmt)
        return list(result.scalars().all())

