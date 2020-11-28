from flask import Flask, url_for, request, render_template
from markupsafe import escape


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # Do the login process
        pass
    else:
        return render_template("login.html")


@app.route('/sign_up')
def sign_up():
    return render_template("sign_up.html")


@app.route('/dashbaord')
def dashbaord():
    return render_template("dashboard/index.html")


app.run(port=8898, debug=True)
