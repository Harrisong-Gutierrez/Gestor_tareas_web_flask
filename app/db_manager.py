from sqlalchemy import text
from datetime import datetime
from config import engine
from app.models import Task

class DBManager:
    def add_task(self, task_data):
        try:
            with engine.begin() as conn:  # ✅ begin() maneja commit automáticamente
                conn.execute(
                    text("""
                        INSERT INTO tasks 
                        (title, description, priority, due_date, task_type, completed, created_at) 
                        VALUES (:title, :description, :priority, :due_date, :task_type, :completed, :created_at)
                    """),
                    {
                        "title": task_data['title'],
                        "description": task_data['description'],
                        "priority": task_data['priority'],
                        "due_date": task_data.get('due_date'),
                        "task_type": task_data.get('task_type', 'normal'),
                        "completed": False,
                        "created_at": datetime.utcnow()
                    }
                )
            return True
        except Exception as e:
            raise e

    def complete_task(self, task_id):
        with engine.begin() as conn:  # ✅ begin() también aquí
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

    def get_tasks(self, sort_by='priority', filter_completed=None):
        query = "SELECT * FROM tasks"
        params = {}

        if filter_completed is not None:
            query += " WHERE completed = :completed"
            params["completed"] = filter_completed

        if sort_by == 'priority':
            query += " ORDER BY priority DESC, created_at"
        elif sort_by == 'date':
            query += " ORDER BY created_at"

        with engine.connect() as conn:
            result = conn.execute(text(query), params)
            tasks = [Task.from_dict(dict(row._mapping)) for row in result]
        return tasks
