import random

from flask import Flask, url_for, escape, render_template, request
from flask_bootstrap import Bootstrap
from .Connection.RedisConn import RedisConn
from .form import SelectYear

app = Flask(__name__, template_folder="../templates")
app.secret_key='test'
bootstrap = Bootstrap(app)


@app.route("/index")
def index():
    return "index"


@app.route("/user/<username>")
def show_user(username):
    return render_template('hello.html', title="user", name=username)


@app.route("/login")
def login() -> str:
    return "login"


@app.route("/mv",methods=['POST','GET'])
def mv():
    form = SelectYear()
    if form.validate_on_submit():
        value=form.year.data
        return str(value)
    else:
        return render_template('formtest.html',form=form)


