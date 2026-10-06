import logging
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import FastAPI, Request, Response
from sqlalchemy import text

from app.config import request_id_ctx, settings, setup_logging
from app.database.connection import AsyncSessionLocal, engine
from app.handlers.exception_handlers import register_exception_handlers
from app.routes import auth_routes, film_routes, review_routes


# Initialize structured JSON logging
setup_logging()
logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("==> [STARTUP] Film Review Platform API Day4 starting up")
    logger.info(f"==> [STARTUP] Loaded configuration: api_version={settings.api_version}")
    logger.info("==> [STARTUP] Schema managed via Alembic migrations")

    yield

    logger.info("==> [SHUTDOWN] Film Review Platform API Day4 shutting down")
    await engine.dispose()
    logger.info("==> [SHUTDOWN] Database engine connection pool disposed")


app = FastAPI(
    title="Film Review Platform API Day4",
    description="FastAPI API with Service Layer, Centralized Exception Handling, and Structured JSON Logging.",
    version="1.0.0",
    lifespan=lifespan,
)


access_logger = logging.getLogger("http_access")


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    """
    Request-scoped middleware that captures or generates a unique request_id,
    propagates it into contextvars for structured logging across the request lifecycle,
    and returns it in the X-Request-ID response header.
    """
    req_id = (
        request.headers.get("X-Request-ID")
        or request.headers.get("X-Trace-ID")
        or str(uuid.uuid4())
    )
    token = request_id_ctx.set(req_id)
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        raw_auth = request.headers.get("authorization")
        auth_preview = (raw_auth[:30] + "...") if raw_auth else "None"
        access_logger.info(
            f"HTTP {request.method} {request.url.path} -> {response.status_code} | Authorization: {auth_preview}"
        )
        return response

    finally:
        request_id_ctx.reset(token)


# Register centralized domain exception handlers
register_exception_handlers(app)


@app.get("/health", tags=["Health"], summary="Health check endpoint")
async def health_check(response: Response) -> Dict[str, Any]:
    db_status = "connected"
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"disconnected ({e})"

    return {
        "status": "ok",
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# Register all routers under /api/v1 prefix
app.include_router(film_routes.router, prefix="/api/v1")
app.include_router(review_routes.router, prefix="/api/v1")
app.include_router(auth_routes.router, prefix="/api/v1")
