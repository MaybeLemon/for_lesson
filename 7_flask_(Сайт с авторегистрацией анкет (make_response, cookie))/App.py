from flask import Flask, render_template, request, make_response, redirect
from getter_ankets_result import AutoAnkets
from navigation import *

app = Flask(__name__)

login = ''
passwd = ''
getter_ankets = AutoAnkets()
data = {'nav': get_nav(app),
        'otvet_auth': '',
        }


@app.errorhandler(404)
def handle_error(error):
    return render_template('error.html', data=data)


@app.route('/', methods=['GET', 'POST'])
def autorize():
    global login, passwd
    data['otvet_auth'] = ''
    data['ankets'] = []
    if request.method == 'GET':
        return render_template('authorize.html', data=data)
    elif request.method == 'POST':
        login = request.form['login']
        passwd = request.form['passwd']
        if getter_ankets.authorize(login, passwd):
            resp = make_response(redirect('/selector'))
            resp.set_cookie('user', 'Authorized')
            return resp
        else:
            data['otvet_auth'] = 'Авторизация не удалась'
            return render_template('authorize.html', data=data)


@app.route('/selector', methods=['GET', 'POST'])
def view_ankets():
    global login, passwd
    if 'user' not in request.cookies:
        data['otvet_auth'] = 'Авторизуйтесь!'
        return render_template('authorize.html', data=data)
    else:
        if login == '' or passwd == '':
            data['otvet_auth'] = 'Авторизуйтесь!'
            return render_template('authorize.html', data=data)
        else:
            getter_ankets.authorize(login, passwd)
    if request.method == 'GET':
        if 'ankets' not in data.keys() or data['ankets'] is None or data['ankets'] == []:
            data['ankets'] = getter_ankets.ankets_view()
        return render_template('ankets_selector.html', data=data)
    elif request.method == 'POST':
        data['id_number'] = request.form.get('id')
        if data['id_number'] and any(data['id_number'] in anketa for anketa in data['ankets']):
            getter_ankets.get_anket_from_user(data['id_number'])
            if getter_ankets.post_data() == '1':
                data['otvet_ankets'] = f'Данные об отправлены'
            else:
                data['otvet_ankets'] = 'Произошла ошибка'
        else:
            data['otvet_ankets'] = 'Такой анкеты нет'
        return render_template('ankets_selector.html', data=data)



if __name__ == "__main__":
    app.run('0.0.0.0', port=5007, debug=False)
