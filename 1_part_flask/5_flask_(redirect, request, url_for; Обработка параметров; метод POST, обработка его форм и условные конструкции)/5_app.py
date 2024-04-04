from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main_page():
    something_text = ''
    if request.method == 'POST':
        something_text = request.form['text']
    if request.args.get('text'):
        something_text = request.args.get('text')
    return render_template('index.html' , text = something_text)



if __name__ == "__main__":
    app.run('0.0.0.0', port=5005, debug=True)