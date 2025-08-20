from enum import Enum
from datetime import datetime


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    @property
    def name(self):
        return {1: "Baja", 2: "Media", 3: "Alta"}[self.value]


class Task:
    def __init__(
        self,
        id,
        title,
        description,
        priority,
        created_at,
        completed=False,
        due_date=None,
        task_type="normal",
    ):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.created_at = created_at
        self.completed = completed
        self.due_date = due_date
        self.task_type = task_type

    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.__dict__}
