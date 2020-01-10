from flask import Flask
import os


def create_app(test_config=None):
    DB = {                                          #  DB = {
        "user": "johnny",                             #      "user": "root",
        "pwd": "toor",  # netstat -anp  #      "pwd": "cPHWFPtp55WE4Z1q",  # netstat -anp
        "host": "192.168.1.103",   #      "host": "cdb-ovrbs6o6.cd.tencentcdb.com",
        "port": 3306,                              #      "port": 10055,
        "db": "test"                               #      "db": "test2"
    }                                               #  }
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='zhengwenqaing',
        DATABASE=f"mysql+pymysql://{DB['user']}:{DB['pwd']}@{DB['host']}:{DB['port']}/{DB['db']}",
        MAX_OVERFLOW=5,   # max_overflow=5 必须大写
    )
    if test_config == None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/heart")
    def hello():
        return "<h1>SUCCESS</h1>"


    from . import db  # ??
    db.init_app(app)
    from .auth import bp
    app.register_blueprint(bp)
    from .blog import bp as blog_bp
    app.register_blueprint(blog_bp)
    app.add_url_rule("/", endpoint="index")  # ??
    return app
