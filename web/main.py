from flask import Flask, url_for, request, render_template, abort, redirect, session, flash
from markupsafe import escape
import requests

TOKEN = "edri"
API_URL = f"http://127.0.0.1:5000/{TOKEN}/"
MAX_LOGIN_ATTEMPT = 10
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


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
            return redirect(url_for("/dashboard"))
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


@app.route('/dashboard')
def dashboard():
    if is_logged_in():
        return render_template("dashboard/index.html")
    else:
        return redirect(url_for("login"))


app.secret_key = TOKEN
app.run(port=8898, debug=True)
