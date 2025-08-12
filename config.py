import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    TASKS_FILE = DATA_DIR / 'tasks.json'