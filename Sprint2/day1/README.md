# Film Review Platform — API Skeleton (Day 1)

Minimal FastAPI API skeleton demonstrating the `Route -> Handler -> Service -> DAO` architecture with Pydantic request models.

## Architecture & Layer Responsibilities

```text
Request (JSON payload validated by Pydantic schemas)
   ↓
Route       (app/routes/)    - URL routing, HTTP methods, path parameter parsing, response dispatching
   ↓
Handler     (app/handlers/)  - Request formatting, orchestration, high-level business payload handling
   ↓
Service     (app/services/)  - Domain business logic layer
   ↓
DAO         (app/daos/)      - Data Access Object layer (placeholder queries/simulated persistence)
```

## Folder Structure

```text
app/
├── main.py
├── schemas/
│   ├── film_schemas.py      - FilmCreate, FilmUpdate
│   ├── review_schemas.py    - ReviewCreate, ReviewUpdate
│   └── auth_schemas.py      - UserRegister, UserLogin
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

From `Sprint2/day1/`:

```powershell
uv run uvicorn app.main:app --reload
```
or:
```powershell
uv run python main.py
```

- **Interactive API Documentation (Swagger)**: http://127.0.0.1:8000/docs
- **ReDoc Documentation**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health
