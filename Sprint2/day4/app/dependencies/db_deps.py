from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provides a request-scoped AsyncSession, automatically closing it upon request completion."""
    async with AsyncSessionLocal() as session:
        yield session
