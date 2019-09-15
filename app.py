from flask import Flask
from EasyG import create_app
app = create_app()


@app.route('/')
def hello_world():
    print(app.config.get('KEY'))
    return 'Hello World!'


if __name__ == '__main__':
    Flask.run(debug=True)
