import uuid

from sqlalchemy.orm import Mapped, mapped_column

from src.models.extra import TaskStatus

from .base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.created)