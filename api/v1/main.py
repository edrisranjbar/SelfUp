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

    @app.route('/tasks')
    def tasks():
        return jsonify(tasks=Task.get_all(), tasks_count=Task.get_count())


    @app.route('/task/<task_id>', methods=["GET"])
    def get_task(task_id):
        if Task.task_exist(task_id):
            task_details = Task.get(task_id)
            return jsonify(task_details),200
        else:
            abort(404)

    @app.route('/task/delete/<task_id>', methods=["GET"])
    def delete_task(task_id):
        return jsonify(result=Task.delete(task_id))

    @app.route('/task/update/<task_id>', methods=["POST"])
    def update_task(task_id):
        # TODO: create update method in task class
        # TODO: return a proper message with result as a boolean
        pass

    @app.route('/task/add', methods=["POST"])
    def add_task():
        Task.add(request.task)
        # TODO: return result and if there is an error; send it

    app.run(debug=True)
