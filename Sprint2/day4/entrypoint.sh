#!/bin/sh
set -e

echo "==> [ENTRYPOINT] Running Alembic database migrations..."
alembic upgrade head

echo "==> [ENTRYPOINT] Running idempotent database seed..."
python -m app.database.seed

echo "==> [ENTRYPOINT] Starting service process: $@"
exec "$@"
