from flask import Flask
from app.app import create_app

# app = create_app(config.dev)
app = create_app()

if __name__ == '__main__':
    Flask.run(app, debug=True)
