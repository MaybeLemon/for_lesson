import requests
from random import randint
from bs4 import BeautifulSoup as bs
import json


class AutoAnkets:
    def __init__(self):
        self.data = {}
        self.url_login = 'https://lk.samgtu.ru/site/login'
        self.url_ankets = 'https://lk.samgtu.ru/questionnaires/questionnaires/answer'
        self.url_answer = 'https://lk.samgtu.ru/questionnaires/questionnaires/suggest'
        self.url_questions = 'https://lk.samgtu.ru/questionnaires/questionnaires/questions'

    def authorize(self, login, passwd):
        resp = requests.get(self.url_login)
        self.headers = {
            'Cookie': resp.headers['Set-Cookie'].split(' ')[0],
            'Referer': 'https://lk.samgtu.ru/site/login'
        }
        data = {
            '_csrf': 'qwerty==',
            'LoginForm[username]': login,
            'LoginForm[password]': passwd,
            'LoginForm[rememberMe]': 1
        }
        requests.post(self.url_login, headers=self.headers, data=data)
        resp_for_check = requests.get(self.url_ankets, headers=self.headers)
        if 'Регистрация' in resp_for_check.text:
            return False
        else:
            return True

    def ankets_view(self):
        response_ankets = requests.get(self.url_ankets, headers=self.headers)
        soup = bs(response_ankets.text, 'html.parser')
        self.ankets = soup.find_all('td', class_='selected-row')
        div_element = soup.find('div', {'id': 'questionnaires-answer'})
        ng_init_value = div_element.get('ng-init')
        if ng_init_value:
            self.initForm_value = ng_init_value.split('(')[1].split(')')[0]
        self.db_ankets = []
        for td in self.ankets:
            ng_click_value = td.attrs.get('ng-click', None).split(', ')[-1][:-1]
            span_text = td.find('span').text
            self.db_ankets.append([ng_click_value, span_text])
        return self.db_ankets

    def get_anket_from_user(self, id_number):
        self.id_number = id_number
        resp_idk = requests.get(
            self.url_answer + '?PersonID=' + self.initForm_value + '&QuestionID=' + self.id_number + '&StudyFormID=1',
            headers=self.headers)
        resp_questions = requests.get(
            self.url_questions + '?PersonID=' + self.initForm_value + '&QuestionID=' + self.id_number + '&i=0' + '&StudyFormID=1',
            headers=self.headers)
        if '_csrf' not in self.headers['Cookie']:
            self.headers['Cookie'] = f'{self.headers["Cookie"]}; {resp_questions.headers["Set-Cookie"]}'
        self.json_data = json.loads(resp_idk.text)
        soup = bs(resp_questions.text, 'html.parser')
        self.csrf_to_post = soup.find('input', {'name': '_csrf'}).get('value')
        questions = soup.findAll('div', class_='question')
        data_for_questions = []
        for x in questions:
            values = []
            type_question = ''
            temp_name = ''
            temp_soup = bs(str(x), 'html.parser')
            temp_values = temp_soup.find_all('input')
            temp_values.pop(0)
            for y in temp_values:
                temp_values_soup = bs(str(y), 'html.parser')
                values.append(temp_values_soup.find('input').get('value'))
                type_question = temp_values_soup.find('input').get('type')
                temp_name = temp_values_soup.find('input').get('name')
            data_for_questions.append([values, type_question, temp_name])
        for x in data_for_questions:
            if '[]' in x[2]:
                self.data[x[2][:-2]] = ""

            self.data[x[2]] = str(randint(int(x[0][0]), int(x[0][-1])))
        self.data['QuestionnairesPersonLinks[0][SpecialityID]'] = self.json_data[0]['SpecialityID']
        self.data['QuestionnairesPersonLinks[0][SpecializationID]'] = self.json_data[0]['SpecializationID']
        self.data['QuestionnairesPersonLinks[1][SpecialityID]'] = self.json_data[0]['SpecialityID']
        self.data['QuestionnairesPersonLinks[1][SpecializationID]'] = self.json_data[0]['SpecializationID']

    def post_data(self):
        self.data['_csrf'] = self.csrf_to_post
        self.headers['Referer'] = "https://lk.samgtu.ru/questionnaires/questionnaires/answer"
        response = requests.post(
            self.url_questions + '?PersonID=' + self.initForm_value + '&QuestionID=' + self.id_number + '&i=1' + '&StudyFormID=1',
            headers=self.headers, data=self.data)
        return response.text
