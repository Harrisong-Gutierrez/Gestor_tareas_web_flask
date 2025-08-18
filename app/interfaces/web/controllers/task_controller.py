# interfaces/web/controllers/task_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app import db
from app.core.use_cases.task_use_cases import TaskUseCases
from app.infrastructure.repositories.task_repository import TaskRepository
from app.core.entities.task import Priority
from app.interfaces.helpers import flash_errors, validate_task_form

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/tasks", methods=["GET", "POST"])
def manage_tasks():
    repo = TaskRepository(db.engine)
    use_case = TaskUseCases(repo)

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        priority_str = request.form.get("priority")
        due_date_str = request.form.get("due_date")
        task_type = request.form.get("task_type", "normal")

        errors, priority_num, due_date = validate_task_form(
            title, description, priority_str, due_date_str
        )

        if not errors:
            task_data = {
                "title": title,
                "description": description,
                "priority": Priority(priority_num),
                "due_date": due_date,
                "task_type": "timed" if task_type == "timed" else "normal",
            }

            success, errors = use_case.add_task(task_data)
            if success:
                flash("Tarea agregada correctamente!", "success")
                return redirect(url_for("main.manage_tasks"))
            else:
                flash_errors(errors)
        else:
            flash_errors(errors)

    # Obtener parámetros de filtrado
    sort_by = request.args.get("sort_by", "priority")
    show_completed = request.args.get("show_completed", "all")

    filters = {"sort_by": sort_by, "show_completed": show_completed}

    tasks = use_case.get_tasks(filters)
    return render_template(
        "tasks.html",
        tasks=tasks,
        Priority=Priority,  # Pasamos la clase Priority al template
        sort_by=sort_by,
        show_completed=show_completed,
    )


@bp.route("/complete_task/<string:task_id>")
def complete_task(task_id):
    repo = TaskRepository(db.engine)
    use_case = TaskUseCases(repo)

    success, error = use_case.complete_task(task_id)
    if success:
        flash("Tarea marcada como completada!", "success")
    else:
        flash(error or "No se pudo encontrar la tarea", "danger")
    return redirect(url_for("main.manage_tasks"))


@bp.route("/delete_task/<string:task_id>")
def delete_task(task_id):
    repo = TaskRepository(db.engine)
    use_case = TaskUseCases(repo)

    success, error = use_case.delete_task(task_id)
    if success:
        flash("Tarea eliminada correctamente!", "success")
    else:
        flash(error or "Error al eliminar la tarea", "danger")
    return redirect(url_for("main.manage_tasks"))
