from enum import Enum


class TaskStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"