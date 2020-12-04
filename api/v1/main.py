from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from config import *
from task import *
from category import *
from result import *
from user import *

if __name__ == "__main__":

    # creating tables if not exists
    Task.create_table()
    Result.create_table()
    Category.create_table()
    User.create_table()

    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app)

    @app.route(f'/{TOKEN}/about')
    def about():
        return jsonify(message=ABOUT)

    @app.route(f'/{TOKEN}/task/all', methods=["POST"])
    def tasks():
        user_id = request.values.get("user_id")
        return jsonify(tasks=Task.get_all(user_id), tasks_count=Task.get_count(user_id))

    @app.route(f'/{TOKEN}/task/<task_id>', methods=["POST"])
    def get_task(task_id):
        user_id = request.values.get('user_id')
        if Task.exist(task_id=task_id, user_id=user_id):
            task_details = Task.get(task_id, user_id)
            return jsonify(task_details)
        else:
            abort(400)

    @app.route(f'/{TOKEN}/task/delete/<task_id>', methods=["DELETE"])
    def delete_task(task_id):
        user_id = request.values.get('user_id')
        if Task.exist(task_id, user_id):
            return jsonify(result=Task.delete(task_id, user_id))
        else:
            abort(400)

    @app.route(f'/{TOKEN}/task/update/<task_id>', methods=["PUT"])
    def update_task(task_id):
        task_name = request.values.get('task_name')
        user_id = request.values.get('user_id')
        if Task.exist(task_id, user_id):
            update_status = Task.update(task_id, task_name, user_id)
            return jsonify(status=update_status)
        else:
            return abort(400)

    @app.route(f'/{TOKEN}/task/add', methods=['POST'])
    def add_task():
        task_name = request.values.get('task_name')
        category_id = request.values.get('category_id')
        user_id = request.values.get('user_id')
        print(task_name)
        if Task.is_task_name_valid(task_name):
            add_task_status = Task.add(task_name, category_id, user_id)
            return jsonify(status=add_task_status)
        else:
            return abort(400)

    # Category routes

    @app.route(f'/{TOKEN}/category/all', methods=['POST'])
    def get_categories():
        user_id = request.values.get('user_id')
        categories = Category.get_all(user_id)
        return jsonify(categories=categories, categories_count=Category.get_count(user_id))

    @app.route(f'/{TOKEN}/category/add', methods=["POST"])
    def add_category():
        name = request.values.get('name')
        user_id = request.values.get('user_id')
        description = request.values.get('description')
        add_status = Category.add(name, description, user_id)
        if add_status:
            return jsonify(status=add_status)
        else:
            abort(400)

    @app.route(f'/{TOKEN}/category/delete/<category_id>', methods=["DELETE"])
    def delete_category(category_id):
        user_id = request.values.get('user_id')
        # check if category exists
        if Category.exist(category_id, user_id):
            delete_status = Category.delete(category_id, user_id)
            return jsonify(status=delete_status)
        else:
            abort(400)

    @app.route(f'/{TOKEN}/category/update/<category_id>', methods=["PUT"])
    def update_category(category_id):
        user_id = request.values.get('user_id')
        # check if category exist
        if Category.exist(category_id, user_id):
            name = request.values.get('name')
            description = request.values.get('description')
            update_status = Category.update(
                category_id=category_id, category_name=name, description=description, user_id=user_id)
            return jsonify(status=update_status)
        else:
            abort(400)

    # Result
    @app.route(f'/{TOKEN}/result/add', methods=["POST"])
    def add_result():
        result = request.values.get('result')
        date = request.values.get('date')
        user_id = request.values.get('user_id')
        add_status = Result.add(result, date, user_id)
        return jsonify(status=add_status)

    @app.route(f'/{TOKEN}/result/delete/<result_id>')
    def delete_result(result_id):
        user_id = request.values.get('user_id')
        return jsonify(status=Result.delete(result_id, user_id))

    @app.route(f'/{TOKEN}/result/update/<result_id>', methods=["PUT"])
    def update_result(result_id):
        result = request.values.get('result')
        date = request.values.get('date')
        user_id = request.values.get('user_id')
        return jsonify(status=Result.update(result_id, result, date, user_id))

    @app.route(f'/{TOKEN}/result/all', methods=["POST"])
    def get_all_results():
        user_id = request.values.get('user_id')
        results = Result.get_all(user_id)
        return jsonify(results=results, results_count=Result.get_count(user_id))

    # User
    @app.route(f'/{TOKEN}/user/add', methods=["POST"])
    def add_user():
        name = request.values.get('name')
        email = request.values.get('email')
        password = request.values.get('password')
        add_user_status = User.add(name, email, password)
        return jsonify(status=add_user_status)

    @app.route(f'/{TOKEN}/user/exists', methods=["POST"])
    def check_user_exists():
        email = request.values.get('email')
        password = request.values.get('password')
        return jsonify(status=User.exists(email, password))

    @app.route(f'/{TOKEN}/user/delete/<user_id>', methods=["DELETE"])
    def delete_user(user_id):
        if User.exists(email=None, password=None, user_id=user_id):
            User.remove(user_id)
            return jsonify(status=True)
        else:
            abort(400)

    app.run(debug=True)
