from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy.orm import sessionmaker
import click

_Base = declarative_base()


# engine =

class User_zwq(_Base):  # 继承declarative_base类
    __tablename__ = 'user_zwq'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), nullable=False)
    pwd = Column(String(64), nullable=False)


def _get_engine():
    # print(current_app.config)
    engine = create_engine(current_app.config['DATABASE'],max_overflow=current_app.config['MAX_OVERFLOW'])
    return engine


def init_db():
    engine = _get_engine()
    _Base.metadata.create_all(engine)


def get_dbsession():

    if 'db_session' not in g:
        engine = _get_engine()
        g.db_session = sessionmaker(bind=engine)
    return g.db_session()


def close_db(e=None):  # ？
    db_session = g.pop("db_session", None)  # ??
    if db_session is not None:
        db_session().close()


@click.command('init-db')
@with_appcontext  # ?
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
