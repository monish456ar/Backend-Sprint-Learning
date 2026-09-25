I am continuing my FastAPI learning project from Day 1.

REFERENCE PROJECT:
- The completed Day 1 project is located in the `day-1` folder.
- Treat the Day 1 project as the starting point and source of truth for the existing architecture, routes, handlers, services, DAOs, naming conventions, and configuration.
- Do NOT redesign the project or create a separate project from scratch.
- Day 2 must be implemented as a continuation of Day 1.

FIRST STEP — COPY DAY 1:
1. Before making any Day 2 changes, create a copy of the entire `day-1` project as `day-2`.
2. The original `day-1` folder must remain unchanged.
3. All Day 2 implementation work must happen inside `day-2`.
4. Preserve the existing Day 1 folder structure and files unless a Day 2 requirement specifically requires a change.
5. After copying, inspect the `day-2` project and confirm that it has the same working structure as Day 1.
6. Do not start implementing Pydantic schemas until the Day 1 project has been successfully copied.

DAY 2 TOPIC:
Pydantic v2 — Schemas & Validation

GOAL:
The Day 1 routing skeleton already exists. Day 2 adds typed Pydantic request and response schemas so that the API boundary between client input/output and the internal application is explicit and strictly validated.

IMPORTANT:
- Continue using the existing Day 1 architecture.
- Do not introduce a database yet.
- Do not introduce PostgreSQL.
- Do not introduce SQLAlchemy.
- Do not introduce Alembic.
- Do not introduce JWT authentication.
- Do not introduce password hashing.
- Do not introduce RBAC.
- Do not add unnecessary business logic.
- Use hardcoded data where the exercise asks for placeholder responses.
- Keep the Routes → Handlers → Services → DAOs architecture from Day 1.
- The purpose of this exercise is Pydantic v2 schemas and validation, not database implementation.

SCHEMA ORGANIZATION:
Create/use a schemas layer following the existing project conventions.

Create appropriate Pydantic schemas for:

1. FILM

Create a Film creation/request schema.

Required fields:
- title
- release_year
- genre
- director

The request schema must validate these fields.

Create a Film response schema.

The response must contain:
- generated id
- title
- release_year
- genre
- director
- a computed field showing how many years ago the film was released

The computed field should be derived from `release_year`, rather than being supplied by the client.

Use Pydantic v2 `@computed_field`.

2. REVIEW

Create a Review creation/request schema.

Required fields:
- film_id
- rating
- review body

Validation requirements:
- `film_id` must be an integer.
- `rating` must be a STRICT integer.
- Rating must be between 1 and 10 inclusive.
- A string such as `"8"` must NOT be silently converted to `8`.
- The review body must contain at least 50 characters.

Create a Review response schema.

The response must include:
- review id
- film id
- rating
- review body
- reviewer's display name
- submission timestamp

The reviewer display name and submission timestamp can be hardcoded for now.

3. USER RESPONSE

Create a User response schema.

It should expose:
- username
- email
- role

It must NOT expose:
- password

Important:
Even if the underlying user data contains a password, the response schema must prevent the password from being returned.

4. STRICT MODE

Strict mode must be enabled on all relevant schemas.

Use Pydantic v2 configuration:

ConfigDict(strict=True)

The goal is to prevent unwanted type coercion.

For example:

release_year: int

must reject:

"2024"

instead of silently converting it to:

2024

Do not rely only on manually checking types. Use Pydantic's strict validation.

5. CROSS-FIELD VALIDATION

At least one schema must validate a relationship between two fields.

Use a realistic example.

For example, create a schema containing:

start_year
end_year

and validate that:

start_year <= end_year

OR use another meaningful two-field validation rule.

Use Pydantic v2 `@model_validator` where appropriate.

The validation must involve the relationship between two fields, not just validation of one individual field.

6. FIELD VALIDATION

Use Pydantic v2 `Field()` for constraints where appropriate.

Examples include:

- rating: 1 through 10
- review body: minimum 50 characters

Prefer declarative Pydantic validation rather than manually checking everything inside routes.

7. MODEL CONFIGURATION

Use appropriate Pydantic v2 `model_config` settings where relevant.

The Day 2 learning also covers:

- `strict=True`
- `from_attributes=True`
- `populate_by_name=True`
- `str_strip_whitespace=True`

Understand their purpose, but DO NOT force these settings into schemas where they are not useful.

For example:
- `str_strip_whitespace=True` can be useful for request schemas containing user-entered strings.
- `from_attributes=True` is useful for response schemas when converting ORM/Python objects into Pydantic models, but there is no database/ORM in this exercise yet.
- `populate_by_name=True` is only useful when aliases are actually being used.
- Do not add configuration just for the sake of demonstrating it.

8. UPDATE AT LEAST TWO DAY 1 ENDPOINTS

Take at least two existing endpoints from the Day 1 project and update them to use typed Pydantic request and response models.

For example:

POST /api/v1/films
- request body should use FilmCreate
- response should use FilmResponse

POST /api/v1/films/{film_id}/reviews
- request body should use ReviewCreate
- response should use ReviewResponse

Use the existing Day 1 route → handler → service structure.

Do not bypass the existing layers by putting business logic directly into the route.

9. HARDCODED DATA

The endpoints do NOT need a database.

For example, the service can return hardcoded data matching the response schema.

The important part is that:

Client JSON
→ Pydantic request validation
→ existing route/handler/service structure
→ hardcoded result
→ Pydantic response validation/serialization
→ JSON response

10. PASSWORD SAFETY

Make sure UserResponse does not contain a password field.

Even if internal data looks like:

{
    "id": 1,
    "username": "monish",
    "email": "monish@gmail.com",
    "role": "admin",
    "password": "secret"
}

the API response must only expose:

{
    "username": "monish",
    "email": "monish@gmail.com",
    "role": "admin"
}

Do not return or log passwords.

11. FASTAPI OPENAPI/DOCS

After implementing the schemas, verify `/docs`.

The Swagger/OpenAPI documentation should show:
- request body schemas
- response schemas
- field types
- validation constraints where applicable

12. TESTING

Test the important validation cases.

At minimum verify:

VALID:
- valid Film creation request
- valid Review creation request
- rating = 1
- rating = 10
- review body with 50+ characters

INVALID:
- release_year = "2024"
- rating = "8"
- rating = 0
- rating = 11
- review body shorter than 50 characters
- invalid cross-field relationship

Also verify that the User response never exposes password.

13. DO NOT OVERENGINEER

This is still a learning exercise.

Do not:
- create unnecessary abstractions
- add a database
- add authentication
- add authorization
- add complex repositories
- add unnecessary dependencies
- rewrite the Day 1 architecture

Keep the implementation simple and aligned with the Day 1 project.

IMPLEMENTATION ORDER:

Follow this order strictly:

STEP 1:
Copy `day-1` → `day-2`.

STEP 2:
Inspect the copied Day 2 project and understand the existing Day 1 structure.

STEP 3:
Create the Pydantic schema files.

STEP 4:
Implement Film request/response schemas.

STEP 5:
Implement Review request/response schemas.

STEP 6:
Implement User response schema.

STEP 7:
Add strict mode and required validation rules.

STEP 8:
Add the cross-field `@model_validator`.

STEP 9:
Update at least two Day 1 endpoints to use request and response schemas.

STEP 10:
Run the FastAPI application and test `/docs`.

STEP 11:
Test valid and invalid requests.

STEP 12:
Verify that Day 1 remains untouched and all Day 2 changes exist only in `day-2`.

At each major step, explain:
- what is being changed
- why it is needed
- how it connects to the Day 1 architecture
- which Pydantic v2 concept is being demonstrated

Do not implement everything at once.

START NOW WITH ONLY STEP 1:
Copy the complete `day-1` project into a new `day-2` folder.

After the copy is complete, stop and show me:
1. the resulting Day 2 folder structure
2. confirmation that Day 1 was not modified
3. the next step we will implement

Do NOT start schema implementation until I explicitly continue.