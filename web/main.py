from flask import Flask, url_for, request, render_template
from markupsafe import escape
import requests

TOKEN = "edri"
API_URL = f"http://127.0.0.1:5000/{TOKEN}/"
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.values.get('email')
        password = request.values.get('password')
        user_exists = requests.post(f"{API_URL}user/exists",
                                    {"email": email, "password": password}).json()["status"]
        if user_exists:
            return "User Exists"
        else:
            return "User not found"

    else:
        return render_template("login.html")


@app.route('/sign_up')
def sign_up():
    return render_template("sign_up.html")


@app.route('/dashbaord')
def dashbaord():
    return render_template("dashboard/index.html")


app.run(port=8898, debug=True)
