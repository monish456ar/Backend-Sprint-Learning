import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Dict
import os

from fastapi import FastAPI, Response, status
from app.config import settings
from app.routes import film_routes, review_routes, auth_routes

logger = logging.getLogger("uvicorn.default")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Structured startup log verifying config loading
    logger.info("==> [STARTUP] Film Review Platform API skeleton starting up")
    logger.info(f"==> [STARTUP] Loaded configuration: api_version={settings.api_version}")
    yield
    # Structured shutdown log
    logger.info("==> [SHUTDOWN] Film Review Platform API skeleton shutting down")


app = FastAPI(
    title="Film Review Platform API Day3",
    description="FastAPI API skeleton demonstrating Configuration & Shared Dependencies (BaseSettings, Depends, trace ID, placeholder DB).",
    version="1.0.0",
    lifespan=lifespan,
)

# print("db_url  =", os.getenv("DATABASE_URL"))

@app.get("/health", tags=["Health"], summary="Health check endpoint")
def health_check(response: Response) -> Dict[str, Any]:
    try:
        return {
            "status": "ok",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# Register all routers under /api/v1 prefix
app.include_router(film_routes.router, prefix="/api/v1")
app.include_router(review_routes.router, prefix="/api/v1")
app.include_router(auth_routes.router, prefix="/api/v1")
