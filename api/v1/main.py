from flask import Flask, jsonify, request, abort

from task import *
from category import *
from result import *

if __name__ == "__main__":

    # creating tables if not exists
    Task.create_table()
    Result.create_table()
    Category.create_table()

    app = Flask(__name__)

    @app.route('/about')
    def about():
        return jsonify(message=config.about), 200

    @app.route('/task/all')
    def tasks():
        return jsonify(tasks=Task.get_all(), tasks_count=Task.get_count())


    @app.route('/task/<task_id>', methods=["GET"])
    def get_task(task_id):
        if Task.exist(task_id):
            task_details = Task.get(task_id)
            return jsonify(task_details),200
        else:
            abort(404)

    @app.route('/task/delete/<task_id>', methods=["GET"])
    def delete_task(task_id):
        return jsonify(result=Task.delete(task_id))

    @app.route('/task/update/<task_id>', methods=["PUT"])
    def update_task(task_id):
        task_name = request.values.get('task_name')
        valid = Task.exist(task_id)
        update_status = Task.update(task_id, task_name)
        if valid:
            if update_status:
                return jsonify(status=update_status), 200
            else:
                return jsonify(status=update_status), 400
        else:
            return jsonify(status=update_status), 404

    @app.route('/task/add', methods=['POST'])
    def add_task():
        task_name = request.values.get('task_name')
        valid = Task.is_task_name_valid(task_name)
        if valid:
            add_task_status = Task.add(task_name)
            return jsonify(status=add_task_status), 200
        else:
            return jsonify(status=False), 400

    # Category routes
    @app.route('/category/all')
    def get_categories():
        categories = Category.get_all()
        return jsonify(categories=categories), 200

    @app.route('/category/add', methods=["POST"])
    def add_category():
        name = request.values.get('name')
        description = request.values.get('description')
        add_status = Category.add(name, description)
        if add_status:
            return jsonify(status=add_status), 200
        else:
            return jsonify(status=add_status), 400

    @app.route('/category/delete/<id>')
    def delete_category(id):
        # check if category exists
        if Category.exist(id):
            delete_status = Category.delete(id)
            if delete_status:
                return jsonify(status=delete_status), 200
            else:
                return jsonify(status=delete_status), 400
        else:
            return jsonify(status=False), 404


    @app.route('/category/update/<category_id>', methods=["PUT"])
    def update_category(category_id):
        # check if category exist
        if Category.exist(category_id):
            name = request.values.get('name')
            description = request.values.get('description')
            update_status = Category.update(category_id, name, description)
            if update_status:
                return jsonify(status=update_status), 200
            else:
                return jsonify(status=update_status), 400
        else:
            return jsonify(status=False), 404

    app.run(debug=True)
