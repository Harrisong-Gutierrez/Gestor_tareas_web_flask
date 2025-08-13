from datetime import datetime
from enum import Enum
from app import db  # Importa solo db, no engine

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.String(36), primary_key=True)  # UUID como string
    description = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=Priority.MEDIUM.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, description, priority=Priority.MEDIUM):
        import uuid
        self.id = str(uuid.uuid4())
        self.description = description
        self.priority = priority.value if isinstance(priority, Priority) else priority
        self.created_at = datetime.utcnow()
        self.completed = False

    def mark_as_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'completed': self.completed
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            description=data['description'],
            priority=Priority(data['priority'])
        )
