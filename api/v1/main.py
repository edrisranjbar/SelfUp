from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from config import *
from task import *
from category import *
from result import *

if __name__ == "__main__":

    # creating tables if not exists
    Task.create_table()
    Result.create_table()
    Category.create_table()

    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app)


    @app.route('/about')
    def about():
        return jsonify(message=about)


    @app.route('/task/all')
    def tasks():
        return jsonify(tasks=Task.get_all(), tasks_count=Task.get_count())


    @app.route('/task/<task_id>', methods=["GET"])
    def get_task(task_id):
        if Task.exist(task_id):
            task_details = Task.get(task_id)
            return jsonify(task_details)
        else:
            abort(400)


    @app.route('/task/delete/<task_id>', methods=["GET"])
    def delete_task(task_id):
        if Task.exist(task_id):
            return jsonify(result=Task.delete(task_id))
        else:
            abort(400)


    @app.route('/task/update/<task_id>', methods=["PUT"])
    def update_task(task_id):
        task_name = request.values.get('task_name')
        update_status = Task.update(task_id, task_name)
        if Task.exist(task_id):
            return jsonify(status=update_status)
        else:
            return abort(400)


    @app.route('/task/add', methods=['POST'])
    def add_task():
        task_name = request.values.get('task_name')
        if Task.is_task_name_valid(task_name):
            add_task_status = Task.add(task_name)
            return jsonify(status=add_task_status)
        else:
            return abort(400)


    # Category routes
    @app.route('/category/all')
    def get_categories():
        categories = Category.get_all()
        return jsonify(categories=categories, categories_count=Category.get_count())


    @app.route('/category/add', methods=["POST"])
    def add_category():
        name = request.values.get('name')
        description = request.values.get('description')
        add_status = Category.add(name, description)
        if add_status:
            return jsonify(status=add_status)
        else:
            abort(400)


    @app.route('/category/delete/<category_id>')
    def delete_category(category_id):
        # check if category exists
        if Category.exist(category_id):
            delete_status = Category.delete(category_id)
            return jsonify(status=delete_status)
        else:
            abort(400)


    @app.route('/category/update/<category_id>', methods=["PUT"])
    def update_category(category_id):
        # check if category exist
        if Category.exist(category_id):
            result = request.values.get('result')
            description = request.values.get('date')
            update_status = Category.update(category_id, result, description)
            return jsonify(status=update_status)
        else:
            abort(400)


    # Result
    @app.route('/result/add', methods=["POST"])
    def get_result():
        result = request.values.get('result')
        date = request.values.get('date')
        add_status = Result.add(result, date)
        return jsonify(status=add_status)


    @app.route('/result/delete/<result_id>')
    def delete_result(result_id):
        return jsonify(status=Result.delete(result_id))


    @app.route('/result/update/<result_id>', methods=["PUT"])
    def update_result(result_id):
        result = request.values.get('result')
        date = request.values.get('date')
        return jsonify(status=Result.update(result_id, result, date))


    @app.route('/result/all')
    def get_all_results():
        results = Result.get_all()
        return jsonify(results=results, results_count=Result.get_count())


    app.run(debug=True)
