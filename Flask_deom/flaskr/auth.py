from functools import wraps
from flask import (
    Blueprint, flash,g, redirect ,render_template, request, session, url_for
)
from werkzeug.security import check_password_hash,generate_password_hash

from .db import get_dbsession,User_zwq

bp = Blueprint("auth",__name__,url_prefix="/auth")
print(__name__)

@bp.route("register",methods = ("GET","POST"))
def register():
    if request.method == "POST":
        print("register.post")
        username = request.form['username']
        pwd = request.form['password']
        db_session = get_dbsession()
        print(db_session)
        error = None  # 判断用户输入及用户已注册后的返回错误信息
        if not username:
            error = '未输入用户名'
        elif not pwd:
            error = '未输入密码'
        elif db_session.query(User_zwq.id).filter_by(username=username).first() is not None:
            error = f"{username} 已经被注册"
        if error is None:
            new_user = User_zwq(username=username, pwd=generate_password_hash(pwd))
            print(username,pwd)
            # 添加到session:
            print(db_session)
            test_str = db_session.add(new_user)
            print(test_str)
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route("login",methods = ("GET","POST"))
def login():
    if request.method is "POST":
        username = request.form['username']
        pwd = request.form['password']
        db_session = get_dbsession()
        error = None  # 判断用户输入及用户已注册后的返回错误信息
        print(db_session)
        user = db_session.query(User_zwq.id,User_zwq.pwd).filter_by(username=username).first()
        print(str(user),type(user))
        if not username:
            error = '未输入用户名'
        elif not pwd:
            error = '未输入密码'
        elif not check_password_hash(user["pwd"],pwd):
            error = "用户名或密码错误"
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')
@bp.before_app_request
def load_loggrd_in_user():
    # print(globals())
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_dbsession().query(User_zwq.id,User_zwq.pwd).filter_by(id=user_id).first()
        print(g.user,type(g.user))

def authorize(func):
    """装饰器判断用户是否登录"""

    @wraps(func)
    def logged(*args, **dic):
        if session.get("user_id") is None:
            # print(f"===>{session.username}<==={func.__name__}")
            return  redirect(url_for("auth.login")) # 装饰器注意返回
        else:
            return func(*args, **dic)

    return logged