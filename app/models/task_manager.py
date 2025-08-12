import json
from pathlib import Path
from datetime import datetime
from app.models.task import Task, TimedTask, Priority

class TaskManager:
    def __init__(self, storage_path):
        self.storage_path = Path(storage_path)
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()

    def get_tasks(self, sort_by='priority', filter_completed=None):
        tasks = self.tasks.copy()
        
        if filter_completed is not None:
            tasks = [task for task in tasks if task.completed == filter_completed]
        
        if sort_by == 'priority':
            tasks.sort(key=lambda x: (-x.priority.value, x.created_at))
        elif sort_by == 'date':
            tasks.sort(key=lambda x: x.created_at)
        elif sort_by == 'completed':
            tasks.sort(key=lambda x: x.completed)
            
        return tasks

    def save_tasks(self):
        tasks_data = [task.to_dict() for task in self.tasks]
        with open(self.storage_path, 'w') as f:
            json.dump(tasks_data, f, indent=2)

    def load_tasks(self):
        if not self.storage_path.exists():
            self.tasks = []
            return

        with open(self.storage_path, 'r') as f:
            tasks_data = json.load(f)
        
        self.tasks = []
        for task_data in tasks_data:
            if task_data.get('type') == 'timed':
                self.tasks.append(TimedTask.from_dict(task_data))
            else:
                self.tasks.append(Task.from_dict(task_data))