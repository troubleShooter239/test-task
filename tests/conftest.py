from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncTransaction

from src.core.db.session import async_session_factory, get_async_session
from src.main import create_application


engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost:5433/test')

app = create_application()

@pytest_asyncio.fixture(scope="session")
async def connection() -> AsyncGenerator[AsyncConnection, None]:
    async with engine.connect() as connection:
        yield connection

        
@pytest_asyncio.fixture()
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncTransaction, None]:
    async with connection.begin() as transaction:
        yield transaction

# Use this fixture to get SQLAlchemy's AsyncSession.
# All changes that occur in a test function are rolled back
# after function exits, even if session.commit() is called
# in inner functions
@pytest_asyncio.fixture()
async def session(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncSession, None]:
    async_session = AsyncSession(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    yield async_session

    await transaction.rollback()

@pytest_asyncio.fixture()
async def client(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async_session = AsyncSession(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )
        async with async_session:
            yield async_session
    
    # Here you have to override the dependency that is used in FastAPI's
    # endpoints to get SQLAlchemy's AsyncSession. In my case, it is
    # get_async_session
    app.dependency_overrides[get_async_session] = override_get_async_session
    yield AsyncClient(app=app, base_url="http://test")
    del app.dependency_overrides[get_async_session]

    await transaction.rollback()
