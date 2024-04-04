import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import json


class Getter:
    def __init__(self):
        self.url_json = 'https://lk.samgtu.ru/api/common/distancelearning'
        self.url_login = 'https://lk.samgtu.ru/site/login'
        self.url_for_num = 'https://lk.samgtu.ru/distancelearning/distancelearning/index'
        self.params = {
            'start': '2022-09-01T00:00:00+04:00',
            'end': '2026-05-30T00:00:00+04:00'
        }
        self.headers = {
            'Referer': 'https://lk.samgtu.ru/distancelearning/distancelearning/index',
        }

    def fix_headers(self, filename, sheetname):
        wb = load_workbook(filename)
        sheet = wb[sheetname]

        for col in sheet.columns:
            col[0].style = 'Pandas'

        wb.save(filename)

    def cookie(self, sessid):
        self.headers['Cookie'] = "PHPSESSID=" + sessid

    def authorize(self, login, passwd):
        resp1 = requests.get(self.url_login)
        self.headers['Cookie'] = resp1.headers['Set-Cookie'].split(' ')[0]
        data = {
            '_csrf': 'qwerty==',
            'LoginForm[username]': login,
            'LoginForm[password]': passwd,
            'LoginForm[rememberMe]': 1
        }
        requests.post(self.url_login, headers=self.headers, data=data)

    def parse(self):
        r = requests.get(self.url_json, params=self.params, headers=self.headers)
        if r.status_code != 200:
            return 0

        req_for_name = requests.get(self.url_for_num, params=self.params, headers=self.headers)
        soup = BeautifulSoup(req_for_name.text, 'html.parser')
        self.info = soup.find('div', class_='current-user__info').text.split(' ')[-1]

        old_data = r.json()
        self.new_data = []


        for urok in old_data:
            name = urok['title']
            date = urok['start'].split('T')[0]
            year = date.split('-')[0]
            month = date.split('-')[1]
            day = date.split('-')[2]
            time_start = urok['start'].split('T')[1][:-3]
            time_end = urok['end'].split('T')[1][:-3]
            try:
                teacher = urok['description'].split('br')[1][1:-1]
            except IndexError:
                teacher = ""
            try:
                urok_type = urok['description'].split('br')[2][9:-10]
            except IndexError:
                urok_type = ""

            self.new_data.append({'Название': name,
                             'День': day,
                             'Месяц': month,
                             'Год': year,
                             'Начало': time_start,
                             'Конец': time_end,
                             'Преподаватель': teacher,
                             'Тип предмета': urok_type})

        if not os.path.isdir('json'): os.mkdir('json')
        if not os.path.isdir('../xlsx'): os.mkdir('xlsx')

        # json
        with open(f"json/data_{self.info}.json", "w", encoding='utf-8') as json_file:
            json.dump(self.new_data, json_file)

        file_xlsx = f'xlsx/расписание_{self.info}.xlsx'
        df = pd.DataFrame(self.new_data)
        df.to_excel(file_xlsx, index=False)

        sheetname = 'Sheet1'
        self.fix_headers(file_xlsx, sheetname)

        return self.new_data
