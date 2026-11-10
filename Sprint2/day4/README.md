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
2. `film_review_test_db_day4`: isolated PostgreSQL database for integration tests.
3. `film_review_redis_day4`: Redis container.
4. `film_review_api_day4`: FastAPI container with hot-reloading on port `8000`.

The API container runs `entrypoint.sh` on every start. It calls
`pre_deployment.sh` to validate `DATABASE_URL`, `TEST_DATABASE_URL`,
`REDIS_URL`, and `TOKEN_SECRET_KEY`, then checks database and Redis
connectivity using `pre_deployment.py`. It applies migrations to the isolated
`film_review_test` database, runs the full pytest suite, and only then migrates
and seeds the application database before starting Uvicorn. Any failed check,
migration, or test exits non-zero and prevents the API from starting.

The test database is separate from the application database so integration
tests cannot truncate application data.

### Option B: Using Local Python with UV

If you have a local PostgreSQL instance or the Docker DB running:

```powershell
cd c:\Users\monish\Desktop\python-learning\Sprint2\day4
uv run uvicorn app.main:app --reload
```

- **Interactive API Documentation (Swagger)**: http://127.0.0.1:8000/docs
- **Health Check & DB Probe**: http://127.0.0.1:8000/health
- **Read Films from PostgreSQL**: `GET http://127.0.0.1:8000/api/v1/films`

## Local AWS Development with Floci

Use these commands to practice S3, Secrets Manager, and SQS against the local
Floci endpoint. They do not target real AWS.

> **Do not use real credentials or secret values in this local exercise.**
> The sample credentials and secret values below are placeholders.

### Prerequisites

- Docker is running.
- Floci is installed and available as the `floci` command.
- AWS CLI is installed and available as the `aws` command.

### Start Floci and configure AWS CLI

Start the local AWS emulator:

```powershell
floci start --verbose
```

The endpoint and local console are:

- API endpoint: `http://localhost:4566`
- Floci console: <http://localhost:4566/_floci/ui>

Configure a named profile. When prompted, use these **local-only** values:

| Setting | Value |
|---|---|
| Profile | `floci-local` |
| Access key | `test` |
| Secret key | `test` |
| Default region | `us-east-1` |
| Default output format | `json` |

```powershell
aws configure --profile floci-local
```

Set reusable values for the commands below:

```powershell
$Profile = "floci-local"
$Endpoint = "http://localhost:4566"
$Aws = @("--profile", $Profile, "--endpoint-url", $Endpoint)
```

The profile is stored in `$HOME\.aws\credentials` and
`$HOME\.aws\config`. These are dummy credentials for Floci only.

### S3: create and inspect a bucket

Create a bucket:

```powershell
$Bucket = "workstream-local-documents"
aws @Aws s3 mb "s3://$Bucket"
```

List buckets using the high-level S3 command or the lower-level S3 API:

```powershell
aws @Aws s3 ls
aws @Aws s3api list-buckets
```

Choose a display format:

```powershell
aws @Aws s3api list-buckets --output json
aws @Aws s3api list-buckets --output table
aws @Aws s3api list-buckets --output text
```

Use JMESPath to display only bucket names and creation dates:

```powershell
aws @Aws s3api list-buckets `
  --query "Buckets[].{BucketName:Name,Created:CreationDate}" `
  --output table
```

`--output` controls presentation. `--query` selects fields for display. Neither
option changes the stored bucket. `Name` is the response field; the bucket name
is a value in that field.

### Secrets Manager: create, list, and retrieve secrets

Create two example secrets using placeholder values:

```powershell
aws @Aws secretsmanager create-secret `
  --name "workstream/local/example" `
  --secret-string "local-placeholder"

aws @Aws secretsmanager create-secret `
  --name "workstream/local/database" `
  --secret-string "local-database-placeholder"
```

List secrets to see their metadata. This does not return their values:

```powershell
aws @Aws secretsmanager list-secrets `
  --query "SecretList[].Name" `
  --output table
```

Retrieve a particular secret:

```powershell
aws @Aws secretsmanager get-secret-value `
  --secret-id "workstream/local/example" `
  --query SecretString `
  --output text
```

`get-secret-value` prints the secret value. Only use the placeholder values in
this exercise, and do not copy real credentials, tokens, or connection strings
into terminal captures or shared documents.

The secret ARN and version ID are generated by Floci and can differ between
runs. `create-secret` creates a resource; `list-secrets` returns resource
metadata; `get-secret-value` retrieves one resource's value.

### SQS: create a queue and process a message

Create the queue and capture its URL from the response:

```powershell
$QueueName = "workstream-local-queue"
$QueueUrl = aws @Aws sqs create-queue `
  --queue-name $QueueName `
  --query QueueUrl `
  --output text

$QueueUrl
```

Send a message:

```powershell
aws @Aws sqs send-message `
  --queue-url $QueueUrl `
  --message-body "WorkStream document upload completed"
```

Receive the message and delete it using the receipt handle returned by that
receive operation:

```powershell
$Response = aws @Aws sqs receive-message `
  --queue-url $QueueUrl `
  --wait-time-seconds 5 `
  --output json | ConvertFrom-Json

if ($Response.Messages) {
    $Message = $Response.Messages[0]
    $Message | Select-Object MessageId, Body

    aws @Aws sqs delete-message `
      --queue-url $QueueUrl `
      --receipt-handle $Message.ReceiptHandle
} else {
    Write-Output "No message was available to receive."
}
```

Verify that no message is currently available:

```powershell
aws @Aws sqs receive-message `
  --queue-url $QueueUrl `
  --wait-time-seconds 1 `
  --output json
```

An empty response is expected after the message is deleted. This deletes the
message, not the queue; the queue remains available for future messages.

### AWS CLI options and terminology

| Option or term | Meaning |
|---|---|
| `--profile floci-local` | Selects the local profile and its credentials and region. |
| `--endpoint-url http://localhost:4566` | Sends the request to Floci instead of an AWS service endpoint. |
| `--output json`, `table`, or `text` | Changes how the response is displayed. |
| `--query "Buckets[].Name"` | Uses JMESPath to select response fields for display. |
| ARN | An Amazon Resource Name identifying a resource. |
| Service | An AWS capability, such as S3, Secrets Manager, or SQS. |
| Resource | An object managed by a service, such as a bucket, secret, or queue. |

An ARN generally has this structure:

```text
arn:partition:service:region:account-id:resource
```

Floci uses a local account ID; values such as ARNs, version IDs, message IDs,
and receipt handles are generated and may change between runs.
