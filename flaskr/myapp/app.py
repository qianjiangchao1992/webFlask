from flask import Flask, url_for, escape,render_template

app = Flask(__name__,template_folder="../templates")


@app.route("/index")
def index():
    return "index"


@app.route("/user/<username>")
def show_user(username):
    return render_template('hello.html',name=username)


@app.route("/login")
def login() -> str:
    return "login"


# with app.test_request_context():
#     print(url_for("index"))
#     print(url_for("login"))
#     print(url_for("login", next="/"))
#     print(url_for("show_user", username="tim"))
#     print(url_for('templates', filename='style.css'))

