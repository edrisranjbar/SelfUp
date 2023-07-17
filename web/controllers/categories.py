from models.task import *
from models.category import *
from models.result import *
from models.user import *
from flask import jsonify, abort


def get_all_categories_db(email):
    user_id = User.get_user_id(email)
    categories = Category.get_all(user_id)
    return jsonify(categories=categories, categories_count=Category.get_count(user_id))


def add_category_db(name, description, email):
    user_id = User.get_user_id(email)
    add_status = Category.add(name, description, user_id)
    if add_status:
        return jsonify(status=add_status)
    else:
        abort(400)


def update_category_db(email, category_id, name, description):
    user_id = User.get_user_id(email)
    # check if category exist
    if Category.exist(category_id, user_id):
        update_status = Category.update(
            category_id=category_id, category_name=name, description=description, user_id=user_id)
        return jsonify(status=update_status)
    else:
        abort(400)


def delete_category_db(email, category_id):
    user_id = User.get_user_id(email)
    # check if category exists
    if Category.exist(category_id, user_id):
        delete_status = Category.delete(category_id, user_id)
        return jsonify(status=delete_status)
    else:
        abort(400)