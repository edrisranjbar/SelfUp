from flask import Flask, jsonify, request

from task import *
from category import *
from result import *

if __name__ == "__main__":

    # creating tables if not exists
    Task.create_table()
    Result.create_table()
    Category.create_table()

    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        # TODO: to return a proper message about this API
        return "hello world"

    @app.route('/tasks')
    def tasks():
        return jsonify(tasks=Task.get_all(), tasks_count=Task.get_count())

    # TODO: add a route for getting a single task

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
