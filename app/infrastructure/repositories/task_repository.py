# infrastructure/repositories/task_repository.py
from sqlalchemy import text
from datetime import datetime
from app.core.entities.task import Task, Priority


class TaskRepository:
    def __init__(self, db_engine):
        self.engine = db_engine

    def save(self, task):
        try:
            with self.engine.begin() as conn:
                task_dict = task.to_dict()

                if isinstance(task_dict["priority"], Priority):
                    task_dict["priority"] = task_dict["priority"].value

                if "created_at" in task_dict and isinstance(
                    task_dict["created_at"], datetime
                ):
                    task_dict["created_at"] = task_dict["created_at"].isoformat()
                if "due_date" in task_dict and isinstance(
                    task_dict["due_date"], datetime
                ):
                    task_dict["due_date"] = task_dict["due_date"].isoformat()

                conn.execute(
                    text(
                        """
                        INSERT INTO tasks 
                        (id, title, description, priority, due_date, task_type, completed, created_at) 
                        VALUES (:id, :title, :description, :priority, :due_date, :task_type, :completed, :created_at)
                    """
                    ),
                    task_dict,
                )
            return True
        except Exception as e:
            print(f"Error saving task: {str(e)}")
            raise e

    def get_by_id(self, task_id):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM tasks WHERE id = :id"), {"id": task_id}
                )
                row = result.fetchone()
                if row:
                    task_data = dict(row._mapping)

                    if isinstance(task_data["priority"], int):
                        task_data["priority"] = Priority(task_data["priority"])

                    if "created_at" in task_data and isinstance(
                        task_data["created_at"], str
                    ):
                        task_data["created_at"] = datetime.fromisoformat(
                            task_data["created_at"]
                        )
                    if (
                        "due_date" in task_data
                        and task_data["due_date"]
                        and isinstance(task_data["due_date"], str)
                    ):
                        task_data["due_date"] = datetime.fromisoformat(
                            task_data["due_date"]
                        )
                    return Task(**task_data)
                return None
        except Exception as e:
            print(f"Error getting task by id: {str(e)}")
            raise e

    def update(self, task):
        try:
            with self.engine.begin() as conn:
                task_dict = task.to_dict()

                if isinstance(task_dict["priority"], Priority):
                    task_dict["priority"] = task_dict["priority"].value

                if "created_at" in task_dict and isinstance(
                    task_dict["created_at"], datetime
                ):
                    task_dict["created_at"] = task_dict["created_at"].isoformat()
                if "due_date" in task_dict and isinstance(
                    task_dict["due_date"], datetime
                ):
                    task_dict["due_date"] = task_dict["due_date"].isoformat()

                result = conn.execute(
                    text(
                        """
                        UPDATE tasks SET
                            title = :title,
                            description = :description,
                            priority = :priority,
                            due_date = :due_date,
                            task_type = :task_type,
                            completed = :completed
                        WHERE id = :id
                    """
                    ),
                    task_dict,
                )
                return result.rowcount > 0
        except Exception as e:
            print(f"Error updating task: {str(e)}")
            raise e

    def complete_task(self, task_id):
        try:
            with self.engine.begin() as conn:
                result = conn.execute(
                    text("UPDATE tasks SET completed = TRUE WHERE id = :id"),
                    {"id": task_id},
                )
                return result.rowcount > 0
        except Exception as e:
            print(f"Error completing task: {str(e)}")
            raise e

    def delete(self, task_id):
        try:
            with self.engine.begin() as conn:
                result = conn.execute(
                    text("DELETE FROM tasks WHERE id = :id"), {"id": task_id}
                )
                return result.rowcount > 0
        except Exception as e:
            print(f"Error deleting task: {str(e)}")
            raise e

    def get_tasks(self, filters):
        query = "SELECT * FROM tasks"
        params = {}

        show_completed = filters.get("show_completed")
        if show_completed == "pending":
            query += " WHERE completed = FALSE"
        elif show_completed == "completed":
            query += " WHERE completed = TRUE"

        sort_by = filters.get("sort_by", "priority")
        if sort_by == "priority":
            query += " ORDER BY priority DESC, created_at"
        elif sort_by == "date":
            query += " ORDER BY created_at"

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params)
                tasks = []
                for row in result:
                    task_data = dict(row._mapping)

                    if isinstance(task_data["priority"], int):
                        task_data["priority"] = Priority(task_data["priority"])

                    if "created_at" in task_data and isinstance(
                        task_data["created_at"], str
                    ):
                        task_data["created_at"] = datetime.fromisoformat(
                            task_data["created_at"]
                        )
                    if (
                        "due_date" in task_data
                        and task_data["due_date"]
                        and isinstance(task_data["due_date"], str)
                    ):
                        task_data["due_date"] = datetime.fromisoformat(
                            task_data["due_date"]
                        )
                    tasks.append(Task(**task_data))
                return tasks
        except Exception as e:
            print(f"Error getting tasks: {str(e)}")
            raise e
