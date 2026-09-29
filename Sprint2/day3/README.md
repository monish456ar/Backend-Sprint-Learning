# Film Review Platform — Configuration & Shared Dependencies (Day 3)

Continuation of the FastAPI Film Review Platform project, focusing on centralized environment configuration, typed `BaseSettings` using `pydantic-settings`, and shared dependencies with FastAPI `Depends()`.

## Architecture & Dependency Injection Flow

```text
.env File
    ↓
pydantic_settings.BaseSettings (app/config.py)
    ↓
settings (single Settings instance)
    ↓
get_config()   [app/dependencies.py] ──┐
                                       │
get_db()       [app/dependencies.py] ──┼──> Depends() ──> Route Handlers
                                       │                  (e.g., GET /api/v1/films)
get_trace_id() [X-Trace-ID Header]   ──┘
```

## Day 3 Concepts Demonstrated

1. **Centralized Environment Configuration (`app/config.py`)**:
   - `Settings` class inherits from `BaseSettings` (`pydantic-settings`).
   - Reads required environment variables from `.env` (`DATABASE_URL`, `TOKEN_SECRET_KEY`, `TOKEN_EXPIRE_MINUTES`, `ALLOWED_CORS_ORIGINS`, `API_VERSION`).
   - Fails fast at application startup if any required configuration is missing.
   - Prevents scattered `os.getenv` or `os.environ` reads throughout the application.

2. **Configuration Dependency (`get_config`)**:
   - Injects the typed `Settings` instance into routes using `Depends(get_config)`.

3. **Placeholder Database Dependency (`get_db`)**:
   - Uses `yield` to demonstrate setup and teardown lifecycle of database sessions.
   - Prepares route signatures for real async database sessions (Day 4) without altering route dependency signatures.

4. **Request Trace ID Dependency (`get_trace_id`)**:
   - Reads the `X-Trace-ID` header from incoming requests.
   - If missing, automatically generates a new UUID4 string.
   - Automatically reflected in Swagger OpenAPI documentation as an HTTP request header parameter.

5. **Applied Dependencies**:
   - Applied `get_config()`, `get_db()`, and `get_trace_id()` to routes:
     - `GET /api/v1/films`
     - `GET /api/v1/films/{film_id}`
     - `GET /api/v1/users/me` (uses `get_config`)
     - `GET /api/v1/films/{film_id}/reviews` (uses `get_config`)

## Folder Structure

```text
day3/
├── .env
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── README.md
├── main.py
├── pyproject.toml
└── app/
    ├── main.py
    ├── config.py            - Centralized BaseSettings configuration
    ├── dependencies/        - Reusable shared dependencies package
    │   ├── __init__.py      - Re-exports get_config, get_db, get_trace_id
    │   ├── config_deps.py   - get_config dependency
    │   ├── db_deps.py       - get_db session dependency (yield)
    │   └── trace_deps.py    - get_trace_id header dependency
    ├── schemas/
    │   ├── film_schemas.py
    │   ├── review_schemas.py
    │   └── auth_schemas.py
    ├── routes/
    │   ├── film_routes.py   - Uses Depends(get_config), Depends(get_db), Depends(get_trace_id)
    │   ├── review_routes.py - Uses Depends(get_config)
    │   └── auth_routes.py   - Uses Depends(get_config)
    ├── handlers/
    ├── services/
    └── dao/
```

## Running the API

### Option A: Using Local Python / UV

```powershell
# From Sprint2/day3
uv sync
uv run uvicorn app.main:app --reload
```

### Option B: Using Docker Compose

```powershell
# From Sprint2/day3
docker compose up --build
```

- **Interactive API Documentation (Swagger)**: http://127.0.0.1:8000/docs
- **ReDoc Documentation**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health
