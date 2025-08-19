from fastapi import APIRouter, HTTPException

from src.core import crud
from src.schemas.tasks import TaskCreate, TaskResponse, TaskUpdate
    
from ..deps import db_d

router = APIRouter(prefix='/tasks', tags=['users'])


@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: db_d):
    """
    ### Создать задачу
    Создаёт новую задачу в системе.

    - **title**: название задачи  
    - **description**: описание задачи (необязательно)  
    - **status**: по умолчанию `"created"`

    #### Пример запроса
    ```json
    {
      "title": "Написать тесты",
      "description": "Покрыть CRUD pytest"
    }
    ```

    #### Возможные ошибки
    - **400**: Неверные данные
    """
    return await crud.create_task(db, task)


@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(task_id: str, db: db_d):
    """
    ### Получить задачу по ID
    Возвращает задачу по её уникальному `UUID`.

    #### Пример запроса
    ```bash
    GET /tasks/550e8400-e29b-41d4-a716-446655440000
    ```

    #### Возможные ошибки
    - **404**: Task not found
    """
    db_task = await crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(db: db_d, skip: int = 0, limit: int = 100, ):
    """
    ### Получить список задач
    Возвращает список задач с пагинацией.

    - **skip**: сколько задач пропустить (по умолчанию 0)  
    - **limit**: сколько задач вернуть (по умолчанию 100)

    #### Пример запроса
    ```bash
    GET /tasks/?skip=0&limit=10
    ```
    """
    return await crud.get_tasks(db, skip=skip, limit=limit)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task: TaskUpdate, db: db_d):
    """
    ### Обновить задачу
    Обновляет название, описание или статус задачи.

    #### Пример запроса
    ```json
    {
      "title": "Новый заголовок",
      "status": "in_progress"
    }
    ```

    #### Возможные ошибки
    - **404**: Task not found
    """
    db_task = await crud.update_task(db, task_id, task)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/{task_id}", response_model=TaskResponse)
async def delete_task(task_id: str, db: db_d):
    """
    ### Удалить задачу
    Удаляет задачу по её `UUID`.

    #### Пример запроса
    ```bash
    DELETE /tasks/550e8400-e29b-41d4-a716-446655440000
    ```

    #### Возможные ошибки
    - **404**: Task not found
    """
    db_task = await crud.delete_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task