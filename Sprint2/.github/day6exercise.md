# Async CRUD + DAO Pattern

## Exercise: Film Review Platform — DAO Layer

The database already contains data, so all direct database interaction is moved behind a DAO layer. The DAO is responsible for database queries, while service functions handle business logic and route handlers handle HTTP requests. The request flow follows **Route → Handler → Service → DAO → Database**.

## What I Learned

Today I learned how to use SQLAlchemy 2.0 async queries with `AsyncSession` and how to retrieve results using `scalar_one_or_none()` for a single record and `scalars().all()` for multiple records. I learned how to type async DAO return values such as `Film`, `list[Film]`, `Film | None`, and `bool` so callers know what to expect. I also understood the DAO pattern and why direct database operations should remain inside the DAO instead of being written in services or route handlers. I learned that DAO methods can return `None` when a record is not found, while the service layer can raise a custom domain exception such as `FilmNotFoundError`. I also understood how `Depends(get_db)` provides the `AsyncSession` at the route level, which is then passed through the handler and service to the DAO.

## DAO Structure

The DAO layer organizes database operations by model:

```text
app/
└── dao/
    ├── film_dao.py
    ├── review_dao.py
    └── user_dao.py
```

`film_dao.py` contains Film-related database operations, `review_dao.py` contains Review-related operations, and `user_dao.py` contains User-related operations.

The important separation is:

```text
Route
  ↓
Handler
  ↓
Service
  ↓
DAO
  ↓
Database
```

The service can call DAO methods, but SQLAlchemy queries such as `select()`, `insert()`, `update()`, and `delete()` remain inside the DAO.

## Result Handling

For a single record:

```python
stmt = select(Film).where(Film.id == film_id)

result = await db.execute(stmt)

film = result.scalar_one_or_none()
```

This returns either a `Film` object or `None`.

For multiple records:

```python
stmt = select(Film)

result = await db.execute(stmt)

films = result.scalars().all()
```

This returns a `list[Film]`.

## Return Type Examples

```python
async def get_film_by_id(...) -> Film | None:
    ...
```

```python
async def get_all_films(...) -> list[Film]:
    ...
```

```python
async def create_film(...) -> Film:
    ...
```

```python
async def delete_film(...) -> bool:
    ...
```

The return type acts as a clear contract for the service calling the DAO.

## Not Found Handling

The DAO can return `None` when a requested record does not exist:

```python
return result.scalar_one_or_none()
```

The service can then decide how the application should handle that case:

```python
film = await film_dao.get_film_by_id(db, film_id)

if film is None:
    raise FilmNotFoundError()

return film
```

This keeps database access in the DAO and application-level decisions in the service.

## Dependency Injection

The database session is provided using FastAPI dependency injection:

```python
db: AsyncSession = Depends(get_db)
```

The session is not created inside the DAO. Instead, it is passed through the application layers:

```text
Route
  ↓ db
Handler
  ↓ db
Service
  ↓ db
DAO
  ↓
PostgreSQL
```

This keeps database connection management separate from database query logic.

## Exercise Requirements

* Build a `FilmDAO` with typed async methods for getting a film by ID, listing films with optional filters, creating a film, updating specified fields, and soft-deleting a film.
* Build a `ReviewDAO` for listing reviews by film, calculating the average rating, creating reviews, and deleting reviews.
* Build a `UserDAO` with a method to find a user by email.
* Pass `AsyncSession` into DAO methods through dependency injection instead of creating sessions inside DAO methods.
* Update at least two route handlers to follow **Route → Handler → Service → DAO**.
