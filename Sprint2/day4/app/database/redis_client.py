import logging
from typing import Optional
import redis.asyncio as aioredis
from app.config import settings

logger = logging.getLogger("app.redis")

# Shared Redis Client configured from centralized settings.
# Uses an internal connection pool and reuses connections across all requests.
redis_client: aioredis.Redis = aioredis.from_url(
    settings.redis_url,
    decode_responses=True,
    max_connections=20,
)


async def init_redis() -> None:
    """Verifies Redis connectivity on application startup."""
    try:
        await redis_client.ping()
        logger.info("==> [STARTUP] Redis connection established successfully at %s", settings.redis_url)
    except Exception as e:
        logger.error("==> [STARTUP] Failed to connect to Redis at %s: %s", settings.redis_url, str(e))
        raise


async def close_redis() -> None:
    """Closes Redis connection pool cleanly on application shutdown."""
    try:
        await redis_client.aclose()
        logger.info("==> [SHUTDOWN] Redis connection closed successfully")
    except Exception as e:
        logger.warning("==> [SHUTDOWN] Error closing Redis connection: %s", str(e))


def get_redis_client() -> aioredis.Redis:
    """Returns the shared Redis client singleton."""
    return redis_client
