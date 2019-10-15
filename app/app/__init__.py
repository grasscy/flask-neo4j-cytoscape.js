import os

from flask import Flask, g
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if not test_config:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

    from . import graph
    from . import db
    app.register_blueprint(graph.bp)

    @app.before_request
    def before_request():
        g.db = db.get_db()

    return app
