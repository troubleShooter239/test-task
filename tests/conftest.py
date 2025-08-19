from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
import pytest_asyncio

from src.main import create_application

app = create_application()

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
