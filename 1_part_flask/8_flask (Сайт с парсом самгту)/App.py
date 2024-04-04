from flask import Flask, render_template, request
import os
import json
from getter import Getter
from scripts import *
from data import give_data
from navigation import *


class WebSite:
    def __init__(self, __name__):
        self.json_folder = None
        self.htmls = None
        self.app = Flask(__name__)
        self.setup_routes()
        self.data = give_data()
        self.data['nav'] = get_nav(self.app)

    def setup_routes(self):
        @self.app.errorhandler(404)
        def handle_error(error):
            return render_template(self.htmls['error'], data=self.data)

        @self.app.route('/', methods=['GET', 'POST'])
        def generate():
            if self.data['otvet']: self.data['otvet'] = ''
            if request.method == 'GET':
                return render_template(self.htmls['generate'], data=self.data)
            elif request.method == 'POST':
                getter = Getter()
                if 'btn1' in request.form:
                    login = request.form['login']
                    passwd = request.form['passwd']
                    getter.authorize(login, passwd)
                    new_data = getter.parse()
                    if new_data != 0:
                        self.data['otvet_auth'] = 'Парсинг прошёл успешно'
                        return render_template(self.htmls['generate'], data=self.data)
                    else:
                        self.data['otvet_auth'] = 'Произошла ошибка'
                        return render_template(self.htmls['generate'], data=self.data)
                elif 'btn2' in request.form:
                    sessid = request.form['sessid']
                    getter.cookie(sessid)
                    new_data = getter.parse()
                    if new_data != 0:
                        self.data['otvet_sessid'] = 'Парсинг прошёл успешно'
                        return render_template(self.htmls['generate'], data=self.data)
                    else:
                        self.data['otvet_sessid'] = 'Произошла ошибка'
                        return render_template(self.htmls['generate'], data=self.data)

        @self.app.route('/selector')
        def view():
            json_files = [f for f in os.listdir(self.json_folder) if f.endswith('.json')]
            self.data['numbers'] = [f.split('_')[1].split('.')[0] for f in json_files]
            return render_template(self.htmls['selector'], data=self.data)

        @self.app.route('/<int:number>', methods=['GET', 'POST'])
        def json_page(number):
            json_file = f'data_{number}.json'
            if os.path.exists(os.path.join(self.json_folder, json_file)):
                with open(os.path.join(self.json_folder, json_file), 'r', encoding='utf-8') as f:
                    lessons = json.load(f)

                self.data['unique_names'] = give_unique_names(lessons)
                self.data['unique_teacher'] = give_unique_teachers(lessons)
                self.data['lessons'] = lessons
                if request.method == 'GET':
                    return render_template(self.htmls['timesheet'], data=self.data)
                elif request.method == 'POST':
                    if 'sort' in request.form:
                        date = request.form['date']
                        sub_type = request.form['sub_type']
                        data = sort_btn(self.data, date, sub_type, lessons)
                        return render_template(self.htmls['timesheet'], data=self.data)

                    elif 'sub_info' in request.form:
                        sub = request.form['sub_name']
                        data = sub_info_btn(self.data, sub, lessons)
                        data['sub_info'] = f'Расписание предмета {sub}'
                        return render_template(self.htmls['timesheet'], data=self.data)

                    elif 'teacher_sub' in request.form:
                        teacher = request.form['teacher_info']
                        data = teacher_sub_btn(self.data, teacher, lessons)
                        data['teacher_info'] = f'Расписание преподавателя {teacher}'
                        return render_template(self.htmls['timesheet'], data=self.data)

                    else:
                        return render_template(self.htmls['timesheet'], data=self.data)
            else:
                return render_template(self.htmls['error'], data=self.data)

    def run(self, host, port, debug):
        self.app.run(host, port=port, debug=debug)

