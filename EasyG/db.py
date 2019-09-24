from py2neo import Graph
from flask import g, current_app


def get_db():
    if 'db' not in g:
        g.db = Graph(current_app.config['DB_URL'], username=current_app.config['DB_NAME'],
                     password=current_app.config['DB_PWD'])
    return g.db
