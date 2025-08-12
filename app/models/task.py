from uuid import uuid4
from datetime import datetime
from enum import Enum

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Task:
    def __init__(self, title, description, priority=Priority.MEDIUM):
        self.id = str(uuid4())
        self.title = title
        self.description = description
        self.priority = priority if isinstance(priority, Priority) else Priority(priority)
        self.created_at = datetime.now()
        self.completed = False

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'created_at': self.created_at.isoformat(),
            'completed': self.completed
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            title=data['title'],
            description=data['description'],
            priority=data['priority']
        )
        task.id = data['id']
        task.created_at = datetime.fromisoformat(data['created_at'])
        task.completed = data['completed']
        return task

class TimedTask(Task):
    def __init__(self, title, description, due_date, priority=Priority.MEDIUM):
        super().__init__(title, description, priority)
        self.due_date = due_date

    def to_dict(self):
        task_dict = super().to_dict()
        task_dict['due_date'] = self.due_date.isoformat() if self.due_date else None
        task_dict['type'] = 'timed'
        return task_dict

    @classmethod
    def from_dict(cls, data):
        task = cls(
            title=data['title'],
            description=data['description'],
            due_date=datetime.fromisoformat(data['due_date']),
            priority=data['priority']
        )
        task.id = data['id']
        task.created_at = datetime.fromisoformat(data['created_at'])
        task.completed = data['completed']
        return task