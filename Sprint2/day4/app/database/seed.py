import asyncio
import logging
from typing import Dict
from sqlalchemy import func, select
from app.database.connection import AsyncSessionLocal
from app.models.film import Film
from app.models.review import Review
from app.models.user import User

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Baseline Seed Data
USERS_DATA = [
    {
        "username": "monish",
        "email": "monish@filmreview.com",
        "password": "hashed_password_123",
        "role": "admin",
    },
    {
        "username": "sarah_critic",
        "email": "sarah@critics.org",
        "password": "hashed_password_456",
        "role": "critic",
    },
    {
        "username": "alex_cinephile",
        "email": "alex@cinephiles.net",
        "password": "hashed_password_789",
        "role": "user",
    },
]

FILMS_DATA = [
    {
        "title": "The Shawshank Redemption",
        "genre": "Drama",
        "release_year": 1994,
        "director": "Frank Darabont",
        "hero": "Tim Robbins",
    },
    {
        "title": "The Godfather",
        "genre": "Crime, Drama",
        "release_year": 1972,
        "director": "Francis Ford Coppola",
        "hero": "Marlon Brando",
    },
    {
        "title": "The Dark Knight",
        "genre": "Action, Crime, Drama",
        "release_year": 2008,
        "director": "Christopher Nolan",
        "hero": "Christian Bale",
    },
    {
        "title": "Pulp Fiction",
        "genre": "Crime, Drama",
        "release_year": 1994,
        "director": "Quentin Tarantino",
        "hero": "John Travolta",
    },
    {
        "title": "Inception",
        "genre": "Action, Sci-Fi",
        "release_year": 2010,
        "director": "Christopher Nolan",
        "hero": "Leonardo DiCaprio",
    },
    {
        "title": "Fight Club",
        "genre": "Drama",
        "release_year": 1999,
        "director": "David Fincher",
        "hero": "Brad Pitt",
    },
    {
        "title": "Forrest Gump",
        "genre": "Drama, Romance",
        "release_year": 1994,
        "director": "Robert Zemeckis",
        "hero": "Tom Hanks",
    },
    {
        "title": "The Matrix",
        "genre": "Action, Sci-Fi",
        "release_year": 1999,
        "director": "Lana & Lilly Wachowski",
        "hero": "Keanu Reeves",
    },
    {
        "title": "Goodfellas",
        "genre": "Biography, Crime, Drama",
        "release_year": 1990,
        "director": "Martin Scorsese",
        "hero": "Ray Liotta",
    },
    {
        "title": "Interstellar",
        "genre": "Adventure, Drama, Sci-Fi",
        "release_year": 2014,
        "director": "Christopher Nolan",
        "hero": "Matthew McConaughey",
    },
]

REVIEWS_DATA = [
    {
        "film_title": "The Shawshank Redemption",
        "username": "sarah_critic",
        "rating": 10,
        "review_body": "An absolute masterpiece of hope, friendship, and resilience. One of the finest cinematic achievements of all time.",
    },
    {
        "film_title": "The Shawshank Redemption",
        "username": "alex_cinephile",
        "rating": 9,
        "review_body": "Deeply emotional storytelling with remarkable performances by Tim Robbins and Morgan Freeman.",
    },
    {
        "film_title": "The Dark Knight",
        "username": "monish",
        "rating": 10,
        "review_body": "Heath Ledger delivers a legendary performance. Nolan redefined comic book cinema forever.",
    },
    {
        "film_title": "Inception",
        "username": "alex_cinephile",
        "rating": 9,
        "review_body": "Mind-bending original concept executed with technical perfection and Hans Zimmer's iconic score.",
    },
    {
        "film_title": "Pulp Fiction",
        "username": "sarah_critic",
        "rating": 9,
        "review_body": "Non-linear storytelling at its absolute best. Quotable dialogue and unforgettable characters.",
    },
    {
        "film_title": "Interstellar",
        "username": "monish",
        "rating": 10,
        "review_body": "Visually and emotionally stunning. An ambitious journey across space and time driven by profound human connection.",
    },
]


async def seed() -> None:
    """Idempotently seeds baseline users, films, and reviews."""
    logger.info("--> Starting database seed...")

    async with AsyncSessionLocal() as session:
        # 1. Seed Users (idempotent: match on username)
        users_map: Dict[str, User] = {}
        users_added = 0
        for u_data in USERS_DATA:
            stmt = select(User).where(User.username == u_data["username"]).limit(1)
            existing_user = (await session.execute(stmt)).scalars().first()
            if existing_user:
                users_map[u_data["username"]] = existing_user
            else:
                user = User(
                    username=u_data["username"],
                    email=u_data["email"],
                    password=u_data["password"],
                    role=u_data["role"],
                )
                session.add(user)
                await session.flush()
                users_map[u_data["username"]] = user
                users_added += 1

        logger.info(f"Users: {users_added} new inserted, {len(USERS_DATA) - users_added} already existed.")

        # 2. Seed Films (idempotent: match on title and release_year)
        films_map: Dict[str, Film] = {}
        films_added = 0
        for f_data in FILMS_DATA:
            stmt = (
                select(Film)
                .where(
                    Film.title == f_data["title"],
                    Film.release_year == f_data["release_year"],
                )
                .limit(1)
            )
            existing_film = (await session.execute(stmt)).scalars().first()
            if existing_film:
                films_map[f_data["title"]] = existing_film
            else:
                film = Film(
                    title=f_data["title"],
                    genre=f_data["genre"],
                    release_year=f_data["release_year"],
                    director=f_data["director"],
                    hero=f_data.get("hero", "Unknown"),
                )
                session.add(film)
                await session.flush()
                films_map[f_data["title"]] = film
                films_added += 1

        logger.info(f"Films: {films_added} new inserted, {len(FILMS_DATA) - films_added} already existed.")

        # 3. Seed Reviews (idempotent: match on film_id and user_id)
        reviews_added = 0
        for r_data in REVIEWS_DATA:
            film = films_map.get(r_data["film_title"])
            user = users_map.get(r_data["username"])
            if not film or not user:
                logger.warning(f"Skipping review for missing film '{r_data['film_title']}' or user '{r_data['username']}'")
                continue

            stmt = (
                select(Review)
                .where(
                    Review.film_id == film.id,
                    Review.user_id == user.id,
                )
                .limit(1)
            )
            existing_review = (await session.execute(stmt)).scalars().first()
            if not existing_review:
                review = Review(
                    film_id=film.id,
                    user_id=user.id,
                    rating=r_data["rating"],
                    review_body=r_data["review_body"],
                )
                session.add(review)
                reviews_added += 1

        logger.info(f"Reviews: {reviews_added} new inserted, {len(REVIEWS_DATA) - reviews_added} already existed.")

        # Commit all changes
        await session.commit()

        # Query total count for confirmation
        total_users = (await session.execute(select(func.count(User.id)))).scalar_one()
        total_films = (await session.execute(select(func.count(Film.id)))).scalar_one()
        total_reviews = (await session.execute(select(func.count(Review.id)))).scalar_one()

        logger.info(f"==> Database State: Users={total_users}, Films={total_films}, Reviews={total_reviews}")
        logger.info("--> Database seed completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed())
