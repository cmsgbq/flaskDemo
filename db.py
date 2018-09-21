import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext



def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        ) 
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# close_db 和 init_db_command 函数需要在应用实例中注册，否则无法使用。 然而，既然我们使用了工厂函数，那么在写函数的时候应用实例还无法使用。代替地， 我们写一个函数，把应用作为参数，在函数中进行注册。
def init_app(app):
    # app.teardown_appcontext() 告诉 Flask 在返回响应后进行清理的时候调用此函数。
    app.teardown_appcontext(close_db)
    # app.cli.add_command() 添加一个新的 可以与 flask 一起工作的命令。
    app.cli.add_command(init_db_command)



if __name__ == '__main__':
    init_db()