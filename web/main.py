from flask import Flask, url_for, request, render_template, abort, redirect, session, flash, jsonify
from markupsafe import escape
import requests
from settings import *

app = Flask(__name__)


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
        user_exists = requests.post(f"{API_URL}user/exists",
                                    {"email": email, "password": password}).json()["status"]
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
        add_user = requests.post(f"{API_URL}user/add", {"name": name,
                                                        "email": email, "password": password}).json()["status"]
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
        tasks = requests.post(f"{API_URL}task/all",
                              {"email": session['email']}).json()
        return jsonify(tasks)


@app.route('/dashboard/task/add', methods=['POST'])
def add_task():
    if is_logged_in:
        task_name = request.values.get('task_name')
        category_id = request.values.get('category_id')
        add_task_status = requests.post(
            f"{API_URL}task/add", {"email": session['email'], "task_name": task_name, "category_id": category_id}).json()
        return jsonify(add_task_status)


@app.route('/dashboard/task/delete/<task_id>')
def delete_task(task_id):
    if is_logged_in():
        delete_status = requests.delete(
            f"{API_URL}task/delete/{task_id}", data={"email": session['email']}).json()
        return jsonify(delete_status)


@app.route('/dashboard/task/update/<task_id>', methods=['PUT'])
def update_task(task_id):
    if is_logged_in():
        task_name = request.values.get('task_name')
        update_task_status = requests.put(
            f"{API_URL}task/update/{task_id}", {"task_name": task_name, "email": session['email']}).json()
        return jsonify(update_task_status)


@app.route('/dashboard/category/all')
def get_all_categories():
    if is_logged_in():
        categories = requests.post(f"{API_URL}category/all",
                                   {"email": session['email']}).json()
        return jsonify(categories)


@app.route('/dashboard/category/add', methods=['POST'])
def add_category():
    if is_logged_in():
        name = request.values.get('name')
        description = request.values.get('description')
        add_category_status = requests.post(
            f"{API_URL}category/add", {"name": name, "description": description, "email": session['email']}).json()
        return jsonify(add_category_status)


@app.route('/dashboard/category/update/<category_id>', methods=['PUT'])
def update_category(category_id):
    if is_logged_in():
        name = request.values.get('name')
        description = request.values.get('description')
        update_category_status = requests.put(
            f"{API_URL}category/update/{category_id}", {"name": name, "description": description, "category_id": category_id, "email": session['email']}).json()
        return jsonify(update_category_status)


@app.route('/dashboard/category/delete/<category_id>')
def delete_category(category_id):
    if is_logged_in():
        delete_category_status = requests.delete(
            f"{API_URL}category/delete/{category_id}", data={"email": session['email']}).json()
        return delete_category_status


@app.route('/dashboard/result/all')
def get_all_results():
    if is_logged_in():
        results = requests.post(
            f"{API_URL}result/all", {"email": session['email']}).json()
        return jsonify(results)


@app.route('/dashboard/result/add', methods=['POST'])
def add_result():
    if is_logged_in():
        result = request.values.get('result')
        date = request.values.get('date')
        results = requests.post(
            f"{API_URL}result/add", {"result": result, "date": date, "email": session['email']}).json()
        return jsonify(results)


app.secret_key = TOKEN
app.run(port=8898, debug=True)
