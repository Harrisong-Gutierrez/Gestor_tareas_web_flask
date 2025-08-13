
from sqlalchemy import text
from datetime import datetime
from config import engine
from app.models import Task, Priority
import uuid  # Importación añadida

class DBManager:
    def add_task(self, task_data):
        try:
            with engine.begin() as conn:
                # Generar UUID si no viene en los datos
                task_id = task_data.get('id', str(uuid.uuid4()))
                
                conn.execute(
                    text("""
                        INSERT INTO tasks 
                        (id, title, description, priority, due_date, task_type, completed, created_at) 
                        VALUES (:id, :title, :description, :priority, :due_date, :task_type, :completed, :created_at)
                    """),
                    {
                        "id": task_id,
                        "title": task_data['title'],
                        "description": task_data['description'],
                        "priority": task_data['priority'].value if isinstance(task_data['priority'], Priority) else task_data['priority'],
                        "due_date": task_data.get('due_date'),
                        "task_type": task_data.get('task_type', 'normal'),
                        "completed": task_data.get('completed', False),
                        "created_at": task_data.get('created_at', datetime.utcnow())
                    }
                )
            return True
        except Exception as e:
            raise e

    def complete_task(self, task_id):
        with engine.begin() as conn:
            result = conn.execute(
                text("UPDATE tasks SET completed = :completed WHERE id = :id"),
                {"completed": True, "id": task_id}
            )
            return result.rowcount > 0

    def delete_task(self, task_id):
        with engine.begin() as conn:
            result = conn.execute(
                text("DELETE FROM tasks WHERE id = :id"),
                {"id": task_id}
            )
            return result.rowcount > 0

    def get_tasks(self, sort_by='priority', show_completed=None):
        query = "SELECT * FROM tasks"
        params = {}

        if show_completed is not None:
            query += " WHERE completed = :completed"
            params["completed"] = show_completed

        if sort_by == 'priority':
            query += " ORDER BY priority DESC, created_at"
        elif sort_by == 'date':
            query += " ORDER BY created_at"

        with engine.connect() as conn:
            result = conn.execute(text(query), params)
            tasks = []
            for row in result:
                task_data = dict(row._mapping)
                task_data['priority'] = Priority(task_data['priority'])
                tasks.append(Task.from_dict(task_data))
            return tasks