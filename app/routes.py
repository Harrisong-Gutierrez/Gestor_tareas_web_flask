from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Priority, Task
from app.db_manager import DBManager
from app.utils.helpers import validate_task_form, flash_errors
from datetime import datetime

bp = Blueprint("main", __name__)
db_manager = DBManager()


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/tasks", methods=["GET", "POST"])
def manage_tasks():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        priority_str = request.form.get("priority")
        due_date = request.form.get("due_date")
        task_type = request.form.get("task_type", "normal")

        errors, priority_num, due_date = validate_task_form(
            title, description, priority_str, due_date
        )

        if not errors:
            try:

                due_date_obj = (
                    datetime.strptime(due_date, "%Y-%m-%d") if due_date else None
                )

                new_task = Task(
                    title=title,
                    description=description,
                    priority=Priority(priority_num),
                    due_date=due_date_obj,
                    task_type="timed" if task_type == "timed" else "normal",
                )

                task_data = new_task.to_dict()
                task_data["created_at"] = new_task.created_at

                if db_manager.add_task(task_data):
                    flash("Tarea agregada correctamente!", "success")
                else:
                    flash("Error al guardar la tarea", "danger")

                return redirect(url_for("main.manage_tasks"))

            except ValueError as e:
                flash(f"Error en los datos: {str(e)}", "danger")
            except Exception as e:
                flash(f"Error inesperado: {str(e)}", "danger")
        else:
            flash_errors(errors)

    
    sort_by = request.args.get("sort_by", "priority")
    show_completed = request.args.get("show_completed", "all")

    filter_completed = None
    if show_completed == "completed":
        filter_completed = True
    elif show_completed == "pending":
        filter_completed = False

    tasks = db_manager.get_tasks(sort_by=sort_by, show_completed=filter_completed)

    return render_template(
        "tasks.html",
        tasks=tasks,
        Priority=Priority,
        sort_by=sort_by,
        show_completed=show_completed,
    )


@bp.route("/complete_task/<string:task_id>")
def complete_task(task_id):
    try:
        if db_manager.complete_task(str(task_id)):
            flash("Tarea marcada como completada!", "success")
        else:
            flash("No se pudo encontrar la tarea", "danger")
    except Exception as e:
        flash(f"Error al completar tarea: {str(e)}", "danger")
    return redirect(url_for("main.manage_tasks"))


@bp.route("/delete_task/<string:task_id>")
def delete_task(task_id):
    try:
        if db_manager.delete_task(str(task_id)):
            flash("Tarea eliminada correctamente!", "success")
        else:
            flash("Error al eliminar la tarea", "danger")
    except Exception as e:
        flash(f"Error al eliminar tarea: {str(e)}", "danger")
    return redirect(url_for("main.manage_tasks"))
