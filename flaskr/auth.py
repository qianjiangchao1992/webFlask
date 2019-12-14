import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


# 注册功能
@bp.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Usernaem  is required'
        elif not password:
            error = 'Password is required'
        elif db.execute("SELECT id from user where username=?", (username,)).fetchone() is not None:
            error = 'User {} is already registed'.format(username)
        if error is None:
            db.execute('insert into user(username, password) VALUES (?,?)',
                       (username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')


# 登陆功能
@bp.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute("select * from user where username=?", (username,)).fetchone()
        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')


# 检查用户ID是否存在session
@bp.before_app_request
def load_logger_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("select * from user where id=?", (user_id,)).fetchone()


# 注销功能
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# 检查必须在g里有user的对象
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('index'))
        else:
            return view(**kwargs)

    return wrapped_view



