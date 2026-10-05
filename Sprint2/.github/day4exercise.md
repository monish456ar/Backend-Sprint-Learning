# PostgreSQL + SQLAlchemy 2.0 Async Setup

**Exercise: Film Review Platform — Async Database Layer**

Carry-forward from Day 3: Continue the existing Film Review Platform project from the previous exercise. Before implementing today's features, clone the existing project/repository into a new working copy or branch and continue from the Day 3 implementation.

## 1. Exercise Goal

Today's exercise replaces the Day 3 placeholder database dependency with a real asynchronous PostgreSQL database layer using SQLAlchemy 2.0.

The focus is only on:

* PostgreSQL connection setup
* `asyncpg` as the asynchronous PostgreSQL driver
* SQLAlchemy 2.0 async engine
* Connection pooling
* `AsyncSession` and `async_sessionmaker`
* SQLAlchemy declarative models
* `Mapped` and `mapped_column()`
* Foreign keys and relationships
* Request-scoped database sessions
* FastAPI `Depends()` integration
* Performing at least one real asynchronous database query
* Returning database results through the existing Pydantic response schemas

The database layer should be wired through the existing application architecture without redesigning the route structure.

## 2. Required Database Configuration

Continue using the configuration object created on Day 3.

The database connection URL should come from the existing settings object.

Example:

```text
DATABASE_URL=postgresql+asyncpg://dev_user:dev_password@localhost:5432/film_review
```

The connection URL uses:

```text
postgresql + asyncpg
```

where:

* `postgresql` identifies the database system.
* `asyncpg` is the asynchronous PostgreSQL driver.

Do not read `DATABASE_URL` directly from environment variables inside the database module.

The flow should remain:

```text
.env
  ↓
Settings
  ↓
settings.database_url
  ↓
SQLAlchemy async engine
```

## 3. Async Database Engine

Create an asynchronous SQLAlchemy engine using `create_async_engine()`.

Example:

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    settings.database_url,
)
```

The engine is responsible for managing database connectivity and the connection pool.

Configure the connection pool appropriately for the development application.

For example:

```python
engine = create_async_engine(
    settings.database_url,
    pool_size=5,
    max_overflow=10,
)
```

The exact pool values can remain simple development values.

Understand that:

```text
pool_size
```

controls the number of regular pooled connections, while:

```text
max_overflow
```

allows additional temporary connections when the regular pool is busy.

Connection pooling is not request rate limiting.

The purpose of the pool is to reuse database connections and control how many database connections can be active.

## 4. Async Session Factory

Create an asynchronous session factory using `async_sessionmaker`.

Example:

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

The important distinction is:

```text
engine
  ↓
manages database connectivity and connection pool

async_sessionmaker
  ↓
creates AsyncSession objects

AsyncSession
  ↓
performs database operations
```

`AsyncSession` represents the database session used during the request.

Use:

```python
expire_on_commit=False
```

so ORM object attributes remain available after a commit without requiring an automatic reload.

## 5. Database Session Dependency

Replace the Day 3 placeholder database dependency with the real asynchronous session.

The dependency should create one session for the request and close it automatically when the request finishes.

Example:

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

The lifecycle should be:

```text
HTTP Request
    ↓
get_db()
    ↓
Create AsyncSession
    ↓
Route / Handler / Service / DAO
    ↓
Database operations
    ↓
Request finishes
    ↓
Session closes
```

The session must not be created globally and shared between requests.

## 6. SQLAlchemy Declarative Base

Create a shared SQLAlchemy declarative base for the ORM models.

Example:

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

Keep the base in the models layer.

A possible structure is:

```text
app/
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── user.py
│   ├── film.py
│   └── review.py
```

`Base` provides the metadata that SQLAlchemy uses to keep track of the application's ORM table definitions.

It is not itself a database table.

## 7. ORM Models

Create SQLAlchemy ORM models for:

* User
* Film
* Review

Use SQLAlchemy 2.0 typed ORM syntax with `Mapped` and `mapped_column()`.

Example:

```python
class Film(Base):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    release_year: Mapped[int]
```

Use appropriate column types and constraints.

The models should include:

* Primary keys
* Required/non-null fields
* Unique constraints where appropriate
* Useful indexes where appropriate
* Default values where appropriate
* Created-at timestamps

The created-at timestamp should be populated automatically when the record is inserted.

Prefer a database-side default for the created-at value rather than manually setting the timestamp in application code.

## 8. `Mapped` and `mapped_column()`

Use the SQLAlchemy 2.0 typed ORM style.

For example:

```python
id: Mapped[int] = mapped_column(primary_key=True)
title: Mapped[str]
```

Understand the difference:

```text
Mapped
  ↓
Describes the Python attribute that is mapped by SQLAlchemy.

mapped_column()
  ↓
Configures the corresponding database column.
```

For example:

```python
email: Mapped[str] = mapped_column(
    unique=True,
    index=True,
)
```

This represents a Python `str` attribute mapped to a database column with uniqueness and an index.

## 9. Review Foreign Keys

The `Review` model must reference both:

* Film
* User

Example:

```python
film_id: Mapped[int] = mapped_column(
    ForeignKey("films.id")
)

user_id: Mapped[int] = mapped_column(
    ForeignKey("users.id")
)
```

The foreign keys create the database-level relationships.

The resulting structure should conceptually be:

```text
reviews
   |
   ├── film_id → films.id
   |
   └── user_id → users.id
```

A review therefore belongs to a specific film and a specific user.

## 10. SQLAlchemy Relationships

Configure ORM relationships between the models.

For example:

```python
class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)

    film_id: Mapped[int] = mapped_column(
        ForeignKey("films.id")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    film: Mapped["Film"] = relationship()
    user: Mapped["User"] = relationship()
```

The important distinction is:

```text
ForeignKey
    ↓
Database-level connection

relationship()
    ↓
Python/ORM-level object connection
```

For example:

```python
review.film
```

can represent the related `Film` ORM object.

And:

```python
review.user
```

can represent the related `User` ORM object.

The exercise should configure the relationships so that a review query can access the related film and user information efficiently.

## 11. Database Session Through FastAPI

Update the existing routes that previously used the Day 3 placeholder session.

The route should now receive a real `AsyncSession`.

Example:

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


@router.get("/films")
async def get_films(
    db: AsyncSession = Depends(get_db),
):
    ...
```

The route should not create the session itself.

FastAPI should resolve the dependency:

```text
Route
  ↓
Depends(get_db)
  ↓
AsyncSession
```

The session can then be passed through the existing application layers:

```text
Route
  ↓
Handler
  ↓
Service
  ↓
DAO
  ↓
AsyncSession
```

The DAO is responsible for performing the actual database operation.

## 12. Real Async Database Query

Update at least one existing route to perform a real asynchronous database query.

For example, retrieve all films.

Use SQLAlchemy 2.0 style queries:

```python
from sqlalchemy import select

stmt = select(Film)

result = await db.execute(stmt)

films = result.scalars().all()
```

Understand the difference between:

```python
stmt = select(Film)
```

and:

```python
result = await db.execute(stmt)
```

`select(Film)` creates the SQLAlchemy statement.

It does not execute the query.

`await db.execute(stmt)` sends the statement through SQLAlchemy to the database.

Then:

```python
result.scalars().all()
```

extracts the actual `Film` ORM objects into a Python list.

The flow is:

```text
select(Film)
    ↓
SQLAlchemy statement
    ↓
await session.execute()
    ↓
asyncpg
    ↓
PostgreSQL
    ↓
SQLAlchemy Result
    ↓
scalars().all()
    ↓
list[Film]
```

## 13. Return Existing Pydantic Response Schemas

Continue using the Pydantic response schemas created on Day 2.

For example:

```python
@router.get(
    "/films",
    response_model=list[FilmResponse],
)
async def get_films(
    db: AsyncSession = Depends(get_db),
):
    ...
```

Configure the response schema with:

```python
model_config = ConfigDict(
    from_attributes=True,
)
```

This allows Pydantic to create the response model from SQLAlchemy ORM objects using their attributes.

The flow becomes:

```text
PostgreSQL
    ↓
SQLAlchemy ORM objects
    ↓
FilmResponse
    ↓
JSON response
```

Do not create a completely new response format just for the database exercise.

The Day 2 API response contract should continue to work.

## 14. Database Table Creation

For development/testing, you may use:

```python
Base.metadata.create_all(...)
```

to create the tables described by the SQLAlchemy models.

Understand that:

```text
Base.metadata.create_all()
```

means:

> Create the tables described by the SQLAlchemy models if they do not already exist.

This is useful for simple development or learning environments.

It is not a replacement for a production database migration workflow.

For example, if the `User` model later changes:

```text
User
 ├── id
 ├── name
 └── email   ← new field
```

an existing production database needs a controlled schema change.

That is where Alembic will be introduced.

The production workflow will be:

```text
SQLAlchemy model changes
        ↓
Alembic migration
        ↓
Migration applied
        ↓
PostgreSQL schema updated
```

Do not implement a complete Alembic migration workflow unless it is required by the current exercise.

## 15. Verify the Database Layer

Run the FastAPI application with PostgreSQL available.

Verify through `/docs` that:

* Existing routes are still available.
* The `/films` endpoint performs a real database query.
* The endpoint returns the existing `FilmResponse` schema.
* The database session is created through `Depends(get_db)`.
* The session is closed automatically after the request.
* SQLAlchemy models are registered with `Base`.
* Foreign keys are created correctly.
* Relationships between Review, Film, and User work as expected.

Test at least one real database read.

For example:

```text
GET /api/v1/films
```

should retrieve films from PostgreSQL rather than returning the previous in-memory placeholder data.

## 16. Expected Architecture

After today's exercise, the relevant structure should look approximately like:

```text
app/
├── main.py
├── config.py
├── dependencies.py
├── database/
│   ├── __init__.py
│   └── connection.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── user.py
│   ├── film.py
│   └── review.py
├── routes/
│   ├── film_routes.py
│   ├── review_routes.py
│   └── auth_routes.py
├── handlers/
├── services/
└── daos/
```

The important database flow is:

```text
.env
 ↓
Settings
 ↓
Async Engine
 ↓
AsyncSession Factory
 ↓
get_db()
 ↓
Depends()
 ↓
Route
 ↓
Handler
 ↓
Service
 ↓
DAO
 ↓
AsyncSession
 ↓
SQLAlchemy
 ↓
asyncpg
 ↓
PostgreSQL
```

## 17. What Is Not Required Today

Do not implement these features unless they are required by the existing project:

* JWT authentication
* Password hashing
* RBAC
* Complex business logic
* Complex transaction management
* Advanced query optimization
* Production deployment
* Complete Alembic migration history

The main goal is to establish the real asynchronous PostgreSQL and SQLAlchemy database foundation.

## 18. Exercise Completion Checklist

[ ] Clone the existing Day 3 project/repository before starting
[ ] Continue from the existing Film Review Platform implementation
[ ] Continue using the existing typed configuration from Day 3
[ ] Configure the SQLAlchemy async engine
[ ] Use `postgresql+asyncpg` as the database URL format
[ ] Configure a basic connection pool
[ ] Create an `async_sessionmaker`
[ ] Configure `expire_on_commit=False`
[ ] Create the real `get_db()` async dependency
[ ] Scope one `AsyncSession` to a single HTTP request
[ ] Automatically close the session after the request
[ ] Create the shared `DeclarativeBase`
[ ] Create User, Film, and Review ORM models
[ ] Use `Mapped` and `mapped_column()`
[ ] Add appropriate primary keys and constraints
[ ] Add automatically populated created-at timestamps
[ ] Add Review → Film foreign key
[ ] Add Review → User foreign key
[ ] Configure SQLAlchemy relationships
[ ] Replace the Day 3 placeholder database dependency
[ ] Keep the existing route structure working
[ ] Pass the session through the application layers to the DAO
[ ] Perform at least one real async database query
[ ] Use SQLAlchemy 2.0 `select()` syntax
[ ] Use `await session.execute()`
[ ] Extract ORM objects with `scalars().all()`
[ ] Return the existing Pydantic response schema
[ ] Configure response schemas with `from_attributes=True` where required
[ ] Verify the API through `/docs`
[ ] Confirm data is being read from PostgreSQL
[ ] Understand the purpose and limitation of `Base.metadata.create_all()`

## 19. Carry-Forward to Day 5

Today's exercise establishes the real asynchronous database foundation for the Film Review Platform.

The Day 3 placeholder:

```python
def get_db():
    yield "placeholder-db-session"
```

has now been replaced by:

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

The application now has:

```text
FastAPI
   ↓
Depends(get_db)
   ↓
AsyncSession
   ↓
SQLAlchemy 2.0
   ↓
asyncpg
   ↓
PostgreSQL
```

The existing route and application layers remain in place.

The next database-focused work can build on this foundation by introducing proper schema migrations with **Alembic**, allowing database schema changes to be tracked and applied safely as the application evolves.
### PostgreSQL with Docker

For this exercise, PostgreSQL will run inside a Docker container instead of being installed directly on the local machine. Docker provides the PostgreSQL database environment, while the FastAPI application connects to it through the exposed PostgreSQL port. SQLAlchemy uses `asyncpg` as the asynchronous driver to communicate with PostgreSQL.

The setup is:

```text
FastAPI
   ↓
SQLAlchemy 2.0
   ↓
asyncpg
   ↓
PostgreSQL Docker Container
   ↓
Database
```

The PostgreSQL container can be started and stopped independently from the FastAPI application, making it easy to use the same database setup during local development.
