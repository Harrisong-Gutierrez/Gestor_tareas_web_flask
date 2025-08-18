# interfaces/web/helpers.py
from flask import flash
from datetime import datetime

def validate_task_form(title, description, priority_str, due_date_str=None):
    errors = []
    priority = None
    due_date = None

    if not title or len(title.strip()) < 3:
        errors.append("El título debe tener al menos 3 caracteres")

    if not description or len(description.strip()) < 5:
        errors.append("La descripción debe tener al menos 5 caracteres")

    try:
        priority = int(priority_str)
        if priority not in [1, 2, 3]:
            errors.append("Prioridad inválida (debe ser 1, 2 o 3)")
    except (ValueError, TypeError):
        errors.append("Prioridad debe ser un número (1, 2 o 3)")

    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            errors.append("Fecha inválida. Use el formato YYYY-MM-DD")

    return errors, priority, due_date

def flash_errors(errors):
    for error in errors:
        flash(error, "danger")