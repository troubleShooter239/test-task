from pydantic import BaseModel

from src.models.extra import TaskStatus
from .base_orm import BaseOrm


class TaskBase(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description:str | None = None
    status: TaskStatus | None = None


class TaskResponse(TaskBase, BaseOrm):
    id: str
    status: TaskStatus
