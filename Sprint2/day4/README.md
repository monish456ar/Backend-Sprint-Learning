# Film Review Platform — PostgreSQL + SQLAlchemy 2.0 Async Setup (Day 4)

Continuation of the FastAPI Film Review Platform project, replacing the Day 3 placeholder database dependency with a real asynchronous PostgreSQL database layer using SQLAlchemy 2.0 and `asyncpg`.

## Architecture & Database Layer Flow

```text
.env File
    ↓
pydantic_settings.BaseSettings (app/config.py)
    ↓
settings.database_url (postgresql+asyncpg://dev_user:dev_password@localhost:5432/film_review)
    ↓
SQLAlchemy 2.0 create_async_engine() (app/database/connection.py)
    ↓
async_sessionmaker(expire_on_commit=False)
    ↓
get_db() [app/dependencies/db_deps.py] (request-scoped async generator with yield)
    ↓
FastAPI Depends(get_db)
    ↓
Route Handlers (app/routes/film_routes.py)
    ↓
Handlers (app/handlers/film_handler.py)
    ↓
Services (app/services/film_service.py)
    ↓
DAO Layer (app/dao/film_dao.py) ──> SQLAlchemy 2.0 async queries (select, execute, scalars)
    ↓
PostgreSQL Database Container
    ↓
SQLAlchemy ORM Objects (app/models/)
    ↓
Pydantic Response Schemas (from_attributes=True)
    ↓
Client JSON Response
```

## Day 4 Concepts Demonstrated

1. **Async Database Engine & Connection Pooling (`app/database/connection.py`)**:
   - Uses `create_async_engine()` connecting via `postgresql+asyncpg`.
   - Configures regular pool size (`pool_size=5`) and burst connection pool (`max_overflow=10`).

2. **Async Session Factory**:
   - `AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)`.
   - `expire_on_commit=False` preserves ORM model attributes after commit without extra queries.

3. **Request-Scoped Session Dependency (`app/dependencies/db_deps.py`)**:
   - Defined using `async with AsyncSessionLocal() as session: yield session`.
   - Guarantees one isolated session per HTTP request, closed automatically after the response finishes.

4. **SQLAlchemy Declarative Base & Models (`app/models/`)**:
   - `Base`: Shared `DeclarativeBase`.
   - `User`: `id`, `username`, `email`, `role`, `created_at`, relationship to `Review`.
   - `Film`: `id`, `title`, `release_year`, `genre`, `director`, `created_at`, relationship to `Review`.
   - `Review`: `id`, `film_id` (FK `films.id`), `user_id` (FK `users.id`), `rating`, `review_body`, `created_at`, relationships to `Film` and `User`.

5. **SQLAlchemy 2.0 Real Async Queries (`app/dao/film_dao.py`)**:
   - `stmt = select(Film).order_by(Film.id)`
   - `result = await db.execute(stmt)`
   - `films = result.scalars().all()`

6. **Pydantic Model Compatibility (`from_attributes=True`)**:
   - `FilmResponse` serializes SQLAlchemy ORM models directly into JSON responses using `model_config = ConfigDict(from_attributes=True)`.

7. **Table Initialization (`app/main.py`)**:
   - Uses `await conn.run_sync(Base.metadata.create_all)` in lifespan startup to ensure all PostgreSQL tables exist.
   - Automatically seeds initial films if the table is empty for instant testing.

## Folder Structure

```text
day4/
├── .dockerignore
├── .env
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── README.md
├── main.py
├── pyproject.toml
├── uv.lock
└── app/
    ├── main.py
    ├── config.py
    ├── database/
    │   └── connection.py
    ├── dependencies/
    │   ├── __init__.py
    │   ├── config_deps.py
    │   ├── db_deps.py
    │   └── trace_deps.py
    ├── models/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── user.py
    │   ├── film.py
    │   └── review.py
    ├── schemas/
    │   ├── film_schemas.py
    │   ├── review_schemas.py
    │   └── auth_schemas.py
    ├── routes/
    │   ├── film_routes.py
    │   ├── review_routes.py
    │   └── auth_routes.py
    ├── handlers/
    │   ├── film_handler.py
    │   ├── review_handler.py
    │   └── auth_handler.py
    ├── services/
    │   ├── film_service.py
    │   ├── review_service.py
    │   └── auth_service.py
    └── dao/
        ├── film_dao.py
        ├── review_dao.py
        └── user_dao.py
```

## Running the API

### Option A: Using Docker Compose (Recommended - includes PostgreSQL)

Ensure Docker Desktop is running:

```powershell
cd c:\Users\monish\Desktop\python-learning\Sprint2\day4
docker compose up --build
```

This launches:
1. `film_review_db_day4`: PostgreSQL container with exposed port `5432`.
2. `film_review_api_day4`: FastAPI container with hot-reloading on port `8000`.

### Option B: Using Local Python with UV

If you have a local PostgreSQL instance or the Docker DB running:

```powershell
cd c:\Users\monish\Desktop\python-learning\Sprint2\day4
uv run uvicorn app.main:app --reload
```

- **Interactive API Documentation (Swagger)**: http://127.0.0.1:8000/docs
- **Health Check & DB Probe**: http://127.0.0.1:8000/health
- **Read Films from PostgreSQL**: `GET http://127.0.0.1:8000/api/v1/films`
