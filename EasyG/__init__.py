import os

from flask import Flask, g
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

    from . import graph, db
    app.register_blueprint(graph.bp)

    @app.before_request
    def before_request():
        g.db = db.get_db()

    return app
