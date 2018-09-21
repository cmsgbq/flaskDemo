
from flask import Flask, url_for, request
app = Flask(__name__)

# route路由
@app.route('/')
def IndexPage():
    return "Index Page"

@app.route('/hello')
def hello():
    return 'Hello, World!'

# 变量规则
# 通过把 URL 的一部分标记为 <variable_name> 就可以在 URL 中添加变量
# 转换器类型包括 string,int,float,path,uuid
@app.route('/user/<username>')
def show_user_name(username):
    return 'User %s' % username
@app.route('/post/<int:post_id>')
def show_post0(post_id):
    return 'Post %d' % post_id

# 唯一URL， 访问一个没有斜杠结尾的 URL 时 Flask 会自动进行重定向
# 访问添加了尾部斜杠则会得到404错误 以保证URL唯一性

#URL反向构建
with app.test_request_context():
    print(url_for('IndexPage'))
    print(url_for('hello'))
    print(url_for('hello', next='/'))
    print(url_for('show_user_name', username='John Doe'))

# HTTP 方法
@app.route('/login1', methods=['GET', 'POST'])
def login0():
    if request.methods == 'POST':
        return 'do_the_login'
    else:
        return 'show_the_login_form'
# 如果当前使用了 GET 方法， Flask 会自动添加 HEAD 方法支持，并且同时还会 按照 HTTP RFC 来处理 HEAD 请求。同样， OPTIONS 也会自动实现。

# 静态文件
# 包或模块旁边创建一个名为 static 的文件夹就行了。 静态文件位于应用的 /static 中
with app.test_request_context():
    print(url_for('static', filename='style.css'))

# 渲染模板, Flask 自动为你配置 Jinja2 模板引擎
# 使用 render_template() 方法可以渲染模板，你只要提供模板名称和需要 作为参数传递给模板的变量就行
from flask import render_template
@app.route('/myt/')
@app.route('/myt/<name>')
def myt(name=None):
    return render_template('my_template.html', name=name)

# 操作请求数据
# 在 Flask 中由全局 对象 request 来提供请求信息
# 通过使用 method 属性可以操作当前请求方法，通过使用 form 属性处理表单数据（在 POST 或者 PUT 请求 中传输的数据）。以下是使用上述两个属性的例子:

@app.route('/login2', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

# 文件上传， 在你的 HTML 表单中设置 enctype="multipart/form-data"
# 已上传的文件被储存在内存或文件系统的临时位置。
# 你可以通过请求对象 files 属性来访问上传的文件。每个上传的文件都储存在这个 字典型属性中。
# 这个属性基本和标准 Python file 对象一样，另外多出一个 用于把上传文件保存到服务器的文件系统中的 save() 方法。
@app.route('/upload0', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')




# Cookies,要访问 cookies ，可以使用 cookies 属性。
# 可以使用响应 对象 的 set_cookie 方法来设置 cookies 
# 请求对象的 cookies 属性是一个包含了客户端传输的所有 cookies 的字典。在 Flask 中，如果使用 会话 ，那么就不要直接使用 cookies ，因为 会话 比较安全一些。

# 读取 cookies:
@app.route('/')
def indexRead():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.

# 储存 cookies:
from flask import make_response

@app.route('/')
def indexSave():
    resp = make_response(render_template('my_template.html'))
    resp.set_cookie('username', 'the username')
    return resp


# 重定向和错误
# 使用 redirect() 函数可以重定向。使用 abort() 可以 更早退出请求，并返回错误代码:

from flask import abort, redirect, url_for

@app.route('/re')
def indexre():
    return redirect(url_for('loginre'))

@app.route('/loginre')
def loginre():
    abort(401)
    'this_is_never_executed()'

# 缺省情况下每种出错代码都会对应显示一个黑白的出错页面。使用 errorhandler() 装饰器可以定制出错页面:
@app.errorhandler(401)
def page_not_found(error):
    return render_template('page_not_found.html'), 401

# 关于响应 以下是转换的规则

# 如果视图返回的是一个响应对象，那么就直接返回它。
# 如果返回的是一个字符串，那么根据这个字符串和缺省参数生成一个用于返回的 响应对象。
# 如果返回的是一个元组，那么元组中的项目可以提供额外的信息。元组中必须至少 包含一个项目，且项目应当由 (response, status, headers) 或者 (response, headers) 组成。 status 的值会重载状态代码， headers 是一个由额外头部值组成的列表或字典。
# 如果以上都不是，那么 Flask 会假定返回值是一个有效的 WSGI 应用并把它转换为 一个响应对象。

# 如果想要在视图内部掌控响应对象的结果，那么可以使用 make_response() 函数

# @app.errorhandler(404)
# def not_found(error):
#     return render_template('error.html'), 404
# 可以使用 make_response() 包裹返回表达式，获得响应对象，并对该对象 进行修改，然后再返回:
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp




# 会话session  相当于用密钥签名加密的cookie ，即用户可以查看你的 cookie ，但是如果没有密钥就无法修改它。
# 使用会话之前你必须设置一个密钥
from flask import Flask, session, redirect, url_for, escape, request

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/indexse')
def indexse():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login5', methods=['GET', 'POST'])
def login5():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('indexse'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('indexse'))





# 消息闪现
#  Flask 通过闪现系统来提供了一个易用的反馈方式。闪现系统的基本工作原理是在请求结束时 记录一个消息，提供且只提供给下一个请求使用。通常通过一个布局模板来展现闪现的 消息。
# flash() 用于闪现一个消息。在模板中，使用 get_flashed_messages() 来操作消息



# 日志
# 因为用户篡改了数据或客户端代码出错 而导致一个客户端代码向服务器发送了明显错误的 HTTP 请求。
# 以下是一些日志调用示例
# app.logger.debug('A value for debugging')
# app.logger.warning('A warning occurred (%d apples)', 42)
# app.logger.error('An error occurred')
# logger 是一个标准的 Logger Logger 类， 更多信息详见官方的 logging 文档

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1113)

