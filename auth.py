import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

# url_prefix指定本蓝图全部视图的前缀URL
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f'User {username} is already registered.'

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            #  url_for() 根据登录视图的名称生成相应的 URL
            return redirect(url_for('auth.login'))
        flash(error)

    # else Get请求：
    return render_template('auth/register.html')



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# 在任何URL请求前运行 验证已经登录后将用户信息读取并存在g.user中
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    # TODO: delect
    print("bp.before_app_request调用 ")
    if user_id is None:
        print("用户未登录")
        g.user = None
    else:
        print("成功后载入用户信息")
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# 在其他视图中做验证 
# [X]TODOs: 猜测被此装饰器 装饰的函数 会先执行load_logged_in_user
# 已验证正确
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # TODO: delect
        print("login_required装饰器验证登录")
        if g.user is None:
            print("用户未登录 重定向")
            return redirect(url_for('auth.login'))
        print("验证OK")
        return view(**kwargs)

    return wrapped_view


# 端点和 URL
# url_for() 函数根据视图名称和发生成 URL 。视图相关联的名称亦称为 端点 ，缺省情况下，端点名称与视图函数名称相同。

# 例如，前文被加入应用工厂的 hello() 视图端点为 'hello' ，可以使用 url_for('hello') 来连接。如果视图有参数，后文会看到，那么可使用 url_for('hello', who='World') 连接。

# 当使用蓝图的时候，蓝图的名称会添加到函数名称的前面。上面的 login 函数 的端点为 'auth.login' ，因为它已被加入 'auth' 蓝图中。

