from flask import Flask, url_for, request, render_template, abort, redirect, session, flash
from database.db import create_all_tables
from controllers.users import check_user_exists, add_new_user
from controllers.tasks import get_all_tasks_db, create_task, delete_task_db, update_task_db
from controllers.categories import get_all_categories_db, add_category_db, update_category_db, delete_category_db
from controllers.results import get_all_results_db, add_result_db
from settings import *

app = Flask(__name__)

create_all_tables()

@app.route('/')
def index():
    return render_template("index.html", title=TITLE)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if "login_attempt" not in session:
            session['login_attempt'] = 0
        else:
            session['login_attempt'] += 1
        if session['login_attempt'] > MAX_LOGIN_ATTEMPT:
            redirect(url_for("login"))
        email = request.values.get('email')
        password = request.values.get('password')
        user_exists = check_user_exists(email, password)
        if user_exists:
            # set session
            session["email"] = email
            flash("You were successfully logged in!", 'success')
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials!", 'error')
            return render_template("login.html")

    else:
        if is_logged_in():
            return redirect(url_for("dashboard"))
        return render_template("login.html")


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if is_logged_in():
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        name = request.values.get('name')
        email = request.values.get('email')
        password = request.values.get('password')
        # TODO: check if user exists, rais error
        add_user = add_new_user(name, email, password)
        if add_user:
            return redirect(url_for("dashboard"))
    return render_template("sign_up.html")


def is_logged_in():
    if "email" in session:
        return True
    return False


@app.route('/logout')
def logout():
    if is_logged_in():
        del session["email"]
        flash("You were successfully logged out!", 'success')
        return redirect(url_for("login"))


# Dashboard routes
@app.route('/dashboard')
def dashboard():
    if is_logged_in():
        return render_template("dashboard/index.html")
    else:
        return redirect(url_for("login"))


@app.route('/dashboard/task/all')
def get_all_tasks():
    if is_logged_in():
        tasks = get_all_tasks_db(session['email'])
        return tasks


@app.route('/dashboard/task/add', methods=['POST'])
def add_task():
    if is_logged_in:
        task_name = request.values.get('task_name')
        category_id = request.values.get('category_id')
        add_task_status = create_task(task_name, category_id, session['email'])
        return add_task_status


@app.route('/dashboard/task/delete/<task_id>')
def delete_task(task_id):
    if is_logged_in():
        delete_status = delete_task_db(session['email'], task_id)
        return delete_status


@app.route('/dashboard/task/update/<task_id>', methods=['PUT'])
def update_task(task_id):
    if is_logged_in():
        task_name = request.values.get('task_name')
        update_task_status = update_task_db(session['email'], task_name, task_id)
        return update_task_status


@app.route('/dashboard/category/all')
def get_all_categories():
    if is_logged_in():
        categories = get_all_categories_db(session['email'])
        return categories


@app.route('/dashboard/category/add', methods=['POST'])
def add_category():
    if is_logged_in():
        name = request.values.get('name')
        description = request.values.get('description')
        add_category_status = add_category_db(name, description, session['email'])
        return add_category_status


@app.route('/dashboard/category/update/<category_id>', methods=['PUT'])
def update_category(category_id):
    if is_logged_in():
        name = request.values.get('name')
        description = request.values.get('description')
        update_category_status = update_category_db(session['email'], category_id, name, description)
        return update_category_status


@app.route('/dashboard/category/delete/<category_id>')
def delete_category(category_id):
    if is_logged_in():
        delete_category_status = delete_category_db(session['email'], category_id)
        return delete_category_status


@app.route('/dashboard/result/all')
def get_all_results():
    if is_logged_in():
        results = get_all_results_db(session['email'])
        return results


@app.route('/dashboard/result/add', methods=['POST'])
def add_result():
    if is_logged_in():
        result = request.values.get('result')
        date = request.values.get('date')
        results = add_result_db(result, date, session['email'])
        return results


app.secret_key = TOKEN
app.run(port=8898, debug=True)
