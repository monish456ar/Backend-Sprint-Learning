# Film Review Platform — Pydantic v2 Schemas & Validation (Day 2)

Continuation of the FastAPI learning project from Day 1, focusing on typed Pydantic v2 request/response schemas, strict mode validation, computed fields, cross-field validation, and response filtering.

## Architecture Flow

```text
Client JSON
    ↓
Pydantic Request Validation (Strict mode & constraints)
    ↓
Route       (app/routes/)    - HTTP endpoints, schema declarations, response_model routing
    ↓
Handler     (app/handlers/)  - Payload unpacking, orchestration, response structuring
    ↓
Service     (app/services/)  - Domain business logic layer
    ↓
DAO         (app/daos/)      - Data Access Object layer (simulated persistence)
    ↓
Pydantic Response Model      - Automatic serialization, computed fields, password safety filtering
    ↓
Client JSON Response
```

## Day 2 Concepts Demonstrated

1. **Strict Mode (`ConfigDict(strict=True)`)**:
   - Disables silent type coercion (e.g., `"2024"` is rejected for `int`, `"8"` is rejected for `rating`).
2. **Computed Fields (`@computed_field`)**:
   - `FilmResponse.years_ago` dynamically computes how many years ago a film was released based on `release_year` without client input.
3. **Field Constraints (`Field(...)`)**:
   - Strict rating between 1 and 10 inclusive (`ge=1, le=10`).
   - Review body minimum length constraint (`min_length=50`).
4. **Cross-Field Validation (`@model_validator(mode="after")`)**:
   - `FilmFilterQuery` verifies that `start_year <= end_year`.
5. **Password Safety & Data Sanitization**:
   - `UserResponse` exposes only `username`, `email`, and `role`. Even if internal records include `password`, it is safely omitted from responses.

## Folder Structure

```text
day2/
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── README.md
├── main.py
├── pyproject.toml
└── app/
    ├── main.py
    ├── schemas/
    │   ├── film_schemas.py      - FilmCreate, FilmResponse, FilmFilterQuery
    │   ├── review_schemas.py    - ReviewCreate, ReviewResponse
    │   └── auth_schemas.py      - UserResponse, UserRegister, UserLogin
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
    └── daos/
        ├── film_dao.py
        ├── review_dao.py
        └── user_dao.py
```

## Running the API

### Option A: Using Docker (Recommended)

1. Make sure **Docker Desktop** is running on your machine.
2. From `Sprint2/day2/`:

```powershell
# Using Docker Compose (includes live-reload on code change)
docker compose up --build

# Or using plain Docker CLI:
docker build -t film-api-day2 .
docker run -p 8000:8000 --name film-api-day2 film-api-day2
```

### Option B: Using Local Python / UV

```powershell
uv run python main.py
# or
uv run uvicorn app.main:app --reload
```

- **Interactive API Documentation (Swagger)**: http://127.0.0.1:8000/docs
- **ReDoc Documentation**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health
