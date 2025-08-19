from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_ping(client: AsyncClient):
    response = await client.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}
