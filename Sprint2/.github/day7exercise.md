# Service Layer + Centralized Exception Handling & Structured Logging

## Exercise: Film Review Platform — Service Layer, Exceptions & Logging

The DAO layer is ready, so the service layer is responsible for applying business rules before calling the DAO. Domain exceptions are used for business-rule violations, while centralized exception handling converts them into consistent HTTP responses. Structured logging is used to record application activity and trace requests using a request ID.

## What I Learned

Today I learned how to use a **Service Layer** to keep business rules separate from route handlers and database operations. I learned how the flow follows **Route → Handler → Service → DAO → Database**, with the service deciding what should happen based on the business rules. I learned how to create custom domain exceptions and raise them from the service when a rule is violated. I also learned how FastAPI's centralized exception handler converts these exceptions into consistent JSON error responses. Finally, I learned Python logging, structured JSON logs, and how a request ID can be included in logs to trace a single request.

## Service Layer

The service layer contains the application's business rules and coordinates the DAO operations.

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

For example, when creating a review, the service can check whether the user has already reviewed the film before asking the DAO to create the review.

```python
existing_review = await review_dao.get_user_review(
    db,
    user_id,
    film_id,
)

if existing_review:
    raise ReviewAlreadyExistsError(user_id, film_id)
```

The service handles the business decision, while the DAO handles the database query.

## Business Rules

The service layer enforces the required business rules:

* A user cannot submit more than one review for the same film.
* Only the user who created a review can update its rating or body.
* A film cannot be soft-deleted while it has active reviews.
* Active reviews are consistently treated as reviews that have not been deleted.

This keeps business rules out of the route handlers and DAO layer.

## Custom Domain Exceptions

Custom exceptions represent business-rule violations.

```python
class FilmNotFoundError(DomainException):
    ...

class ReviewAlreadyExistsError(DomainException):
    ...

class ReviewNotOwnerError(DomainException):
    ...

class FilmHasActiveReviewsError(DomainException):
    ...
```

The service raises these exceptions when a business rule is violated.

```python
if existing_review:
    raise ReviewAlreadyExistsError(user_id, film_id)
```

The service does not create an HTTP response. It only reports what went wrong.

## Centralized Exception Handling

FastAPI uses a centralized exception handler to convert domain exceptions into HTTP responses.

```text
Service
  ↓
raise DomainException
  ↓
FastAPI Exception Handler
  ↓
JSON HTTP Response
```

For example:

```python
@app.exception_handler(ReviewAlreadyExistsError)
async def review_exists_handler(
    request: Request,
    exc: ReviewAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={
            "type": "ReviewAlreadyExists",
            "message": exc.message,
            "detail": "User has already reviewed this film.",
        },
    )
```

Route handlers do not need `try/except` blocks for these domain errors.

## Structured Logging

Python logging is used to record application activity.

```python
logger.debug("Starting film creation")

logger.info("Film created successfully")

logger.warning("Film title already exists")

logger.error("Failed to save film")
```

Different levels describe different situations:

```text
DEBUG     → Detailed internal information
INFO      → Normal successful activity
WARNING   → Unusual situation
ERROR     → Operation failed
CRITICAL  → Serious application failure
```

Structured logging stores log information as JSON so that log systems can search and filter individual fields.

Example:

```json
{
  "level": "INFO",
  "timestamp": "2026-10-05T10:30:00Z",
  "logger": "film_service",
  "message": "Film created successfully"
}
```

The JSON formatter is responsible for converting the logging record into this structured format.

## Request-Scoped Logging

A request ID is attached to logs produced during the same request lifecycle.

```text
Request
  ↓
request_id = "abc123"
  ↓
Handler
  ↓
Service
  ↓
DAO
```

Logs from that request can contain the same ID:

```json
{
  "level": "INFO",
  "message": "Creating film",
  "request_id": "abc123"
}
```

```json
{
  "level": "INFO",
  "message": "Film created successfully",
  "request_id": "abc123"
}
```

This makes it possible to search for `request_id = abc123` and follow everything that happened during that request.

## Logging Example

For a film creation operation, the logs can represent different stages:

```python
logger.debug("Starting film creation")

logger.warning("Film title already exists")

logger.info("Film created successfully")

logger.error("Failed to save film because of database error")
```

The logs describe what happened, while the service and exception handler are responsible for the application's actual behavior.

## Exercise Requirements

* Build `FilmService` and `ReviewService` to implement the required business rules.
* Prevent a user from submitting more than one review for the same film.
* Allow only the review owner to update the rating and body.
* Prevent soft-deleting a film while it has active reviews.
* Create typed custom domain exceptions for each business-rule violation.
* Register centralized FastAPI exception handlers that return consistent JSON containing `type`, `message`, and `detail`.
* Keep domain-error `try/except` blocks out of route handlers.
* Configure structured JSON logging with a log level, ISO-8601 timestamp, logger name, and message.
* Include the request ID in logs so that all logs from one request can be traced together.
* Keep the implementation simple while maintaining the flow **Route → Handler → Service → DAO → Database**.
