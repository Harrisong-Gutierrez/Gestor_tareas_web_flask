from datetime import datetime
from enum import Enum
from app import db

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    @property
    def name(self):
        names = {1: "Baja", 2: "Media", 3: "Alta"}
        return names[self.value]

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=Priority.MEDIUM.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)
    task_type = db.Column(db.String(20), default='normal')

    def __init__(self, title, description, priority=Priority.MEDIUM, due_date=None, task_type='normal'):
        import uuid
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority.value if isinstance(priority, Priority) else priority
        self.created_at = datetime.utcnow()
        self.completed = False
        self.due_date = due_date
        self.task_type = task_type

    def mark_as_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'completed': self.completed,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'task_type': self.task_type
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            title=data['title'],
            description=data['description'],
            priority=Priority(data['priority']),
            due_date=data.get('due_date'),
            task_type=data.get('task_type', 'normal')
        )
        if 'completed' in data:
            task.completed = data['completed']
        return task