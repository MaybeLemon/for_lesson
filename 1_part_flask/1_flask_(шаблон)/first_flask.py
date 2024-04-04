# это начальный шаблон сайта на flask

from flask import Flask

app = Flask(__name__)

@app.route('/')
def main_page():
    return 'Добро пожаловать на главную страницу сайта!'

@app.route('/hello')
def hello():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run('0.0.0.0', port=5001, debug=True)