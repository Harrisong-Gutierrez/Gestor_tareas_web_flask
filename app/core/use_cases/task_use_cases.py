# core/use_cases/task_use_cases.py
import uuid
from datetime import datetime
from app.core.entities.task import Priority, Task

class TaskUseCases:
    def __init__(self, task_repository):
        self.repository = task_repository

    def add_task(self, task_data):
        errors = self._validate_task(task_data)
        if errors:
            return False, errors

        task = Task(
            id=str(uuid.uuid4()),
            title=task_data["title"],
            description=task_data["description"],
            priority=Priority(task_data["priority"]),
            created_at=datetime.utcnow(),
            due_date=task_data.get("due_date"),
            task_type=task_data.get("task_type", "normal"),
        )
        return self.repository.save(task), None

    def complete_task(self, task_id):
        task = self.repository.get_by_id(task_id)
        if not task:
            return False, "Task not found"
        
        task.mark_as_completed()
        return self.repository.update(task), None

    def delete_task(self, task_id):
        task = self.repository.get_by_id(task_id)
        if not task:
            return False, "Task not found"
        
        return self.repository.delete(task_id), None

    def get_tasks(self, filters=None):
        """Obtiene tareas aplicando filtros"""
        if filters is None:
            filters = {}
        return self.repository.get_tasks(filters)

    def _validate_task(self, task_data):
        errors = []
        
        if not task_data.get("title") or len(task_data["title"].strip()) < 3:
            errors.append("El título debe tener al menos 3 caracteres")

        if not task_data.get("description") or len(task_data["description"].strip()) < 5:
            errors.append("La descripción debe tener al menos 5 caracteres")

        try:
            priority = int(task_data.get("priority", 2))
            if priority not in [1, 2, 3]:
                errors.append("Prioridad inválida (debe ser 1, 2 o 3)")
        except (ValueError, TypeError):
            errors.append("Prioridad debe ser un número (1, 2 o 3)")

        if "due_date" in task_data and task_data["due_date"]:
            try:
                datetime.strptime(task_data["due_date"], "%Y-%m-%d")
            except ValueError:
                errors.append("Fecha inválida. Use el formato YYYY-MM-DD")

        return errors