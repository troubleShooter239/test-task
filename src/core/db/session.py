from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..config import settings

async_engine = create_async_engine(
    settings.db.url_async,
    # pool_size=5,
    # max_overflow=10,
)
async_session_factory = async_sessionmaker(
    async_engine,
    autocommit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as async_session:
        yield async_session
