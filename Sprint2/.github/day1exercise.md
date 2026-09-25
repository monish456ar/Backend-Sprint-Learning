Create a **minimal FastAPI API skeleton** that satisfies the provided “Film Review Platform — API Skeleton” exercise.

### Goal

Build only the structural foundation required by the exercise. **Do not implement real database operations, PostgreSQL, SQLAlchemy, Alembic, JWT authentication, RBAC, or complex business logic yet.** All endpoints should return simple clearly labelled placeholder responses.

### Requirements

Use a **uv-managed FastAPI project** with this layered structure:

```text
app/
├── main.py
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

The DAO layer should exist because the exercise requires a data-access layer, but **do not connect it to a real database yet**.

### Routers

Create three `APIRouter` modules:

1. Films
2. Reviews
3. Auth/Users

Register all routers in `main.py` using a consistent `/api/v1` prefix.

### Required endpoints

#### Films

```text
GET    /api/v1/films
GET    /api/v1/films/{film_id}
POST   /api/v1/films
PATCH  /api/v1/films/{film_id}
DELETE /api/v1/films/{film_id}
```

#### Reviews

```text
GET    /api/v1/films/{film_id}/reviews
POST   /api/v1/films/{film_id}/reviews
PATCH  /api/v1/reviews/{review_id}
DELETE /api/v1/reviews/{review_id}
```

#### Auth/Users

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/users/me
GET  /api/v1/admin/stats
```

Every endpoint must exist and return a simple, clearly labelled placeholder response. Use path parameters where required.

### Health check

Add:

```text
GET /health
```

It must be publicly accessible and return:

* API status
* Current server timestamp

Example:

```json
{
  "status": "ok",
  "timestamp": "..."
}
```

### Application lifespan

Use FastAPI's modern `lifespan` approach with `@asynccontextmanager`.

Print/log a simple structured message when:

* The application starts
* The application shuts down

Do not use the deprecated `@app.on_event()` approach.

### OpenAPI documentation

Give each router an appropriate tag so `/docs` groups the endpoints by domain:

```text
Films
Reviews
Auth / Users
```

### Keep the implementation simple

Do NOT add:

* PostgreSQL
* SQLAlchemy
* Alembic
* JWT implementation
* password hashing
* authentication middleware
* RBAC implementation
* real database models
* complex Pydantic schemas
* repository patterns
* dependency-injection frameworks
* unnecessary abstractions
* real CRUD logic

The purpose is only to demonstrate:

```text
Route
  ↓
Handler
  ↓
Service
  ↓
DAO
```

and make the complete API surface visible in `/docs`.

After generating the project, briefly explain how the folders and request flow satisfy each requirement of the exercise.
