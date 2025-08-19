from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.tasks import Task
from src.schemas.tasks import TaskCreate, TaskUpdate


async def create_task(db: AsyncSession, task: TaskCreate):
    db_task = Task(title=task.title, description=task.description)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_task(db: AsyncSession, task_id: str):
    return (await db.execute(select(Task).filter(Task.id == task_id))).scalar_one_or_none()


async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100):
    return (await db.execute(select(Task).offset(skip).limit(limit))).scalars().all()


async def update_task(db: AsyncSession, task_id: str, task_update: TaskUpdate):
    db_task = await get_task(db, task_id)
    if not db_task:
        return None

    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)

    await db.commit()
    await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, task_id: str):
    db_task = await get_task(db, task_id)
    if not db_task:
        return None

    await db.delete(db_task)
    await db.commit()
    return db_task