from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main_page():
    something_list = [{"id":1, "name":"something1"}, {"id":2, "name":"something2"}, {"id":3, "name":"something3"}]
    return render_template('index.html', something_list=something_list)


if __name__ == "__main__":
    app.run('0.0.0.0', port=5006, debug=True)