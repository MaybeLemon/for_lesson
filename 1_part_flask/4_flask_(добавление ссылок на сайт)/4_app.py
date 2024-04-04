from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
    something_text = 'Это какой-то текст, подключённый из python'
    return render_template('index.html' , text = something_text)

@app.route('/hello')
def hello():
    return render_template('hello.html')

if __name__ == "__main__":
    app.run('0.0.0.0', port=5004, debug=True)