FastAPI Dependency Injection & Configuration

Exercise: Film Review Platform --- Configuration & Shared Dependencies

Carry-forward from Day 2: Continue the existing Film Review
Platform project from the previous exercise. Before implementing
today's features, clone the existing project/repository into a new
working copy or branch and continue from the Day 2 implementation.

1. Exercise Goal

Today's exercise adds configuration and shared dependencies to the
existing Film Review Platform API.

The focus is only on:

Centralized environment configuration

BaseSettings

FastAPI Depends()

A placeholder database session dependency

Request trace ID dependency

Reusing dependencies in existing routes

Checking the dependency declarations in Swagger /docs

A real database is not required today.

2. Required Configuration

Create a dedicated configuration module.

The module should load the following values from .env:

DATABASE_URL
TOKEN_SECRET_KEY
TOKEN_EXPIRE_MINUTES
ALLOWED_CORS_ORIGINS
API_VERSION

Use BaseSettings from pydantic-settings.

Example .env for development:

DATABASE_URL=postgresql+asyncpg://dev_user:dev_password@localhost:5432/film_review
TOKEN_SECRET_KEY=dev-secret-key
TOKEN_EXPIRE_MINUTES=30
ALLOWED_CORS_ORIGINS=http://localhost:3000
API_VERSION=v1

These are dummy development values. PostgreSQL does not need to be
running for this exercise.

3. Typed Configuration

Create one typed configuration class.

Example:

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    token_secret_key: str
    token_expire_minutes: int
    allowed_cors_origins: str
    api_version: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

The application should use this single settings object instead of
reading environment variables throughout the codebase.

The flow is:

.env
  ↓
BaseSettings
  ↓
Settings()
  ↓
single settings object

Required configuration should fail during application startup if a
required value is missing.

Extra variables in .env are not the problem. The fail-fast behavior
applies when a required setting declared in Settings is missing.

4. Configuration Dependency

Create a dependency that provides the configuration object.

Example:

from app.config import settings


def get_config():
    return settings

Routes that need configuration should receive it through Depends().

Example:

from fastapi import Depends


@router.get("/films")
def get_films(config=Depends(get_config)):
    return {
        "api_version": config.api_version
    }

The route does not read .env directly.

5. Placeholder Database Dependency

A real database is not required for today's exercise.

Create the database dependency structure so it can later be replaced by
a real async database session.

Example:

def get_db():
    yield "placeholder-db-session"

A route can receive it with:

@router.get("/films")
def get_films(db=Depends(get_db)):
    return {
        "message": "Films",
        "db": db
    }

The important requirement is that the dependency uses yield.

Later, the placeholder can be replaced with the real async database
session without changing the route dependency structure.

For example, today's:

get_db()
  ↓
placeholder session
  ↓
route

Later:

get_db()
  ↓
real async database session
  ↓
route

Do not add PostgreSQL, SQLAlchemy, Alembic, or real database queries
in this exercise.

6. Request Trace ID Dependency

Create a dependency that reads a trace identifier from an incoming
request header.

Use a header such as:

X-Trace-ID

The dependency should:

Read the X-Trace-ID header.

Use the incoming value if it exists.

Generate a fresh identifier if the header is missing.

Return the identifier to the route.

Example:

from uuid import uuid4
from fastapi import Header


def get_trace_id(x_trace_id: str | None = Header(default=None)):
    return x_trace_id or str(uuid4())

A route can then use:

@router.get("/films")
def get_films(trace_id=Depends(get_trace_id)):
    return {
        "trace_id": trace_id
    }

7. Apply All Three Dependencies

Apply these dependencies to at least two existing route handlers:

get_config()
get_db()
get_trace_id()

Example:

@router.get("/films")
def get_films(
    config=Depends(get_config),
    db=Depends(get_db),
    trace_id=Depends(get_trace_id),
):
    return {
        "message": "Films",
        "api_version": config.api_version,
        "db": db,
        "trace_id": trace_id,
    }

Apply the same dependency structure to another existing route.

For example:

@router.get("/films/{film_id}")
def get_film(
    film_id: int,
    config=Depends(get_config),
    db=Depends(get_db),
    trace_id=Depends(get_trace_id),
):
    return {
        "film_id": film_id,
        "api_version": config.api_version,
        "db": db,
        "trace_id": trace_id,
    }

The responses can remain simple because the purpose of this exercise is
the dependency structure.

8. Verify Swagger /docs

Run the FastAPI application and open:

/docs

Check the routes that use the dependencies.

Verify that:

The routes are still available.

The X-Trace-ID header appears as a request parameter because it is
declared through the dependency.

The dependency declarations are correctly represented in the
generated OpenAPI documentation.

The configuration and database dependencies are resolved by FastAPI
rather than being sent by the client.

The client should not send a database session or configuration
object.

9. Expected Architecture

After today's exercise, the relevant structure should look approximately
like:

app/
├── main.py
├── config.py
├── dependencies.py
├── routes/
│   ├── film_routes.py
│   ├── review_routes.py
│   └── auth_routes.py
├── handlers/
├── services/
└── daos/

The exact filenames can follow the existing project structure.

The important separation is:

.env
 ↓
Settings
 ↓
get_config()
 ↓
Depends()

get_db()
 ↓
placeholder DB session
 ↓
Depends()

X-Trace-ID
 ↓
get_trace_id()
 ↓
Depends()

10. What Is Not Required Today

Do not implement these features yet:

PostgreSQL setup

SQLAlchemy setup

Alembic migrations

Real database queries

Real async database sessions

JWT authentication

Password hashing

RBAC

Complex business logic

The database dependency is intentionally a placeholder so the real async
session can be added later without redesigning the route signatures.

11. Exercise Completion Checklist

[ ] Clone the existing Day 2 project/repository before starting
[ ] Continue from the existing Film Review Platform implementation
[ ] Create a dedicated configuration module
[ ] Add a .env file with dummy development values
[ ] Use BaseSettings from pydantic-settings
[ ] Define all required configuration fields
[ ] Create one settings object
[ ] Avoid environment-variable reads outside the configuration module
[ ] Create get_config() dependency
[ ] Create placeholder get_db() dependency using yield
[ ] Create get_trace_id() dependency
[ ] Read X-Trace-ID when provided
[ ] Generate a trace ID when the header is missing
[ ] Apply all three dependencies to at least two existing routes
[ ] Run the application
[ ] Verify the routes through /docs
[ ] Confirm X-Trace-ID appears in the OpenAPI request parameters
[ ] Confirm no real database is required

12. Carry-Forward to Day 4

Today's database dependency is only a placeholder.

On Day 4, the placeholder:

def get_db():
    yield "placeholder-db-session"

can be replaced with the real async database session.

The goal is that the route signatures do not need to be redesigned when
the real database is introduced.

The dependency layer therefore provides the boundary between the route
and the actual database implementation.