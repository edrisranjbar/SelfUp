from models.task import *
from models.category import *
from models.result import *
from models.user import *
from flask import jsonify, abort

def get_all_tasks_db(email):
    user_id = User.get_user_id(email)
    return jsonify(tasks=Task.get_all(user_id), tasks_count=Task.get_count(user_id))

def create_task(task_name, category_id, email):
    user_id = User.get_user_id(email)
    if Task.is_task_name_valid(task_name):
        add_task_status = Task.add(task_name, category_id, user_id)
        return jsonify(status=add_task_status)
    else:
        return abort(400)
    
def delete_task_db(email, task_id):
    user_id = User.get_user_id(email)
    if Task.exist(task_id, user_id):
        return jsonify(result=Task.delete(task_id, user_id))
    else:
        abort(400)

def update_task_db(email, task_name, task_id):
    user_id = User.get_user_id(email)
    if Task.exist(task_id, user_id):
        update_status = Task.update(task_id, task_name, user_id)
        return jsonify(status=update_status)
    else:
        return abort(400)