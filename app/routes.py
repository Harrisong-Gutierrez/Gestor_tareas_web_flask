from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Priority
from app.db_manager import DBManager
from app.utils.helpers import validate_task_form, flash_errors
from datetime import datetime

bp = Blueprint('main', __name__)
db_manager = DBManager()

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        due_date = request.form.get('due_date')
        task_type = request.form.get('task_type')
        
        errors, priority, due_date = validate_task_form(title, description, priority, due_date)
        
        if not errors:
            task_data = {
                'title': title,
                'description': description,
                'priority': priority,
                'due_date': due_date if task_type == 'timed' else None,
                'task_type': task_type if task_type == 'timed' else 'normal'
            }
            
            db_manager.add_task(task_data)
            flash('Tarea agregada correctamente!', 'success')
            return redirect(url_for('main.manage_tasks'))
        else:
            flash_errors(errors)
    
    sort_by = request.args.get('sort_by', 'priority')
    show_completed = request.args.get('show_completed', 'all')
    
    if show_completed == 'completed':
        tasks = db_manager.get_tasks(sort_by, True)
    elif show_completed == 'pending':
        tasks = db_manager.get_tasks(sort_by, False)
    else:
        tasks = db_manager.get_tasks(sort_by)
    
    return render_template('tasks.html', 
                         tasks=tasks, 
                         Priority=Priority,
                         sort_by=sort_by,
                         show_completed=show_completed)

@bp.route('/complete_task/<uuid:task_id>')
def complete_task(task_id):
    if db_manager.complete_task(task_id):
        flash('Tarea marcada como completada!', 'success')
    else:
        flash('No se pudo encontrar la tarea', 'danger')
    return redirect(url_for('main.manage_tasks'))

@bp.route('/delete_task/<uuid:task_id>')
def delete_task(task_id):
    if db_manager.delete_task(task_id):
        flash('Tarea eliminada correctamente!', 'success')
    else:
        flash('Error al eliminar la tarea', 'danger')
    return redirect(url_for('main.manage_tasks'))