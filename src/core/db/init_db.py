from loguru import logger

from src.models.base import Base
from .session import async_engine


async def initialize_db() -> None:
    async with async_engine.begin() as conn:
        logger.debug("Dropping all tables")
        await conn.run_sync(Base.metadata.drop_all)
        logger.debug("Creating database tables")
        await conn.run_sync(Base.metadata.create_all)
