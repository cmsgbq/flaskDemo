import os

from flask import Flask , url_for


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_pyfile(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError as e:
        print(e)

    @app.route('/hello')
    def hello():
        return 'Hello World!'
    
    # 注册datebase
    from . import db
    db.init_app(app)
    #db.init_db()

    # 注册蓝图 包括注册蓝图内部 全部注册了路由视图
    from . import auth
    app.register_blueprint(auth.bp)

    # 博客蓝图 内部没设置url_prefix访问URL前缀
    from . import blog
    app.register_blueprint(blog.bp)
    # 除了在blog蓝图中将blog.index绑定'/' （在调用url_for()正常返回'/'）
    # 将blog中index视图的 url_for('index') 也返回URL指向 '/'
    app.add_url_rule('/', endpoint='index')

    # 与验证蓝图不同，博客蓝图没有 url_prefix 。因此 index 视图会用于 / ， create 会用于 /create 
    # 但是，下文的 index 视图的端点会被定义为 blog.index 。一些验证视图 会指定向普通的 index 端点。 我们使用 app.add_url_rule() 关联端点名称 'index' 和 / URL ，这样 url_for('index') 或 url_for('blog.index') 都会有效，会生成同样的 / URL 



    return app


# if __name__ == '__main__':
#     app = create_app()
#     app.run(
#         port=1122
#     )

# export FLASK_APP=flaskr
# export FLASK_ENV=development
# flask run --port=1122
# flask init-db
