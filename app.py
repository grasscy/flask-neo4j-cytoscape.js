from flask import Flask
from EasyG import create_app

app = create_app()

if __name__ == '__main__':
    Flask.run(app, debug=True)
