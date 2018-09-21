import os

from flask import Flask  


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATEBASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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
    

    from . import db
    db.init_app(app)
    #db.init_db()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        port=1122
    )
    
    
