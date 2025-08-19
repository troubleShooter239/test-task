from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_ping(client: AsyncClient):
    response = await client.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


# ---------- Тесты ----------

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    response = await client.post(
        "/api/v1/tasks/",
        json={"title": "Test Task", "description": "Testing create"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "created"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_task(client: AsyncClient):
    # сначала создаём задачу
    create_res = await client.post(
        "/api/v1/tasks/",
        json={"title": "Get Me"}
    )
    task_id = create_res.json()["id"]

    # потом получаем
    res = await client.get(f"/api/v1/tasks/{task_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == task_id
    assert data["title"] == "Get Me"


@pytest.mark.asyncio
async def test_list_tasks(client: AsyncClient):
    # создаём две задачи
    await client.post("/api/v1/tasks/", json={"title": "Task 1"})
    await client.post("/api/v1/tasks/", json={"title": "Task 2"})

    res = await client.get("/api/v1/tasks/?skip=0&limit=10")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 2


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient):
    # создаём задачу
    create_res = await client.post(
        "/api/v1/tasks/",
        json={"title": "Old Title"}
    )
    task_id = create_res.json()["id"]

    # обновляем
    update_res = await client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "New Title", "status": "in_progress"}
    )
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["title"] == "New Title"
    assert updated["status"] == "in_progress"


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):
    # создаём задачу
    create_res = await client.post(
        "/api/v1/tasks/",
        json={"title": "Delete Me"}
    )
    task_id = create_res.json()["id"]

    # удаляем
    delete_res = await client.delete(f"/api/v1/tasks/{task_id}")
    assert delete_res.status_code == 200

    # проверяем что её больше нет
    get_res = await client.get(f"/api/v1/tasks/{task_id}")
    assert get_res.status_code == 404