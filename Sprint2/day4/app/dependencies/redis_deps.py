import redis.asyncio as aioredis
from app.database.redis_client import redis_client


async def get_redis() -> aioredis.Redis:
    """Provides the shared Redis client across requests."""
    return redis_client
