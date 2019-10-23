from flask import Flask
from . import create_app
from instance import config

app = create_app(config.dev)
# app = create_app()

if __name__ == '__main__':
    Flask.run(app, debug=True)
