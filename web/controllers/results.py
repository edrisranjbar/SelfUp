from models.task import *
from models.category import *
from models.result import *
from models.user import *
from flask import jsonify, abort

def get_all_results_db(email):
    user_id = User.get_user_id(email)
    results = Result.get_all(user_id)
    return jsonify(results=results, results_count=Result.get_count(user_id))


def add_result_db(result, date, email):
    user_id = User.get_user_id(email)
    add_status = Result.add(result, date, user_id)
    return jsonify(status=add_status)