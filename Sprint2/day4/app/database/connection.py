from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.config import settings

# 1. Asynchronous SQLAlchemy Engine with Connection Pooling
engine = create_async_engine(
    settings.database_url,
    pool_size=5,
    max_overflow=10,
    echo=False,
)

# 2. Asynchronous Session Factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    
    class_=AsyncSession,
    expire_on_commit=False,
)
