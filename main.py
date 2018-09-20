# -*- coding: UTF-8 -*-
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


# Cookies


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1112)