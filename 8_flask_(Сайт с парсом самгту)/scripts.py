def give_unique_names(lessons):
    unique_names = set()

    for item in lessons:
        unique_names.add(item['Название'])

    sorted_names = sorted(list(unique_names), key=lambda x: x)

    return sorted_names

def give_unique_teachers(lessons):
    unique_teacher = set()

    for item in lessons:
        teach = item['Преподаватель']
        if len(teach.split(', ')) > 1:
            for x in teach.split(', '):
                unique_teacher.add(x)
        else:
            unique_teacher.add(item['Преподаватель'])

    sorted_teachers = sorted(list(unique_teacher), key=lambda x: x)
    sorted_teachers.remove('')
    return sorted_teachers



def sort_btn(data, date, sub_type, lessons):
    if date == "":
        if sub_type == 'nontype':
            return data

        else:
            data['lessons'] = []
            for lesson in lessons:
                if lesson['Тип предмета'] == sub_type:
                    data['lessons'].append(lesson)
            return data

    elif sub_type == 'nontype':
        data['lessons'] = []
        for lesson in lessons:
            if date.split('-') == [lesson['Год'], lesson['Месяц'], lesson['День']]:
                data['lessons'].append(lesson)
        data['lessons'] = sorted(data['lessons'], key=lambda x: int(x['Начало'][:2]))
        return data

    else:
        data['lessons'] = []
        for lesson in lessons:
            if lesson['Тип предмета'] == sub_type and date.split('-') == [lesson['Год'],
                                                                          lesson['Месяц'],
                                                                          lesson['День']]:
                data['lessons'].append(lesson)
        return data

def sub_info_btn(data, sub, lessons):
    data['lessons'] = []
    for lesson in lessons:
        if lesson['Название'] == sub:
            data['lessons'].append(lesson)
    return data

def teacher_sub_btn(data, teacher, lessons):
    data['lessons'] = []
    for lesson in lessons:
        if teacher in lesson['Преподаватель']:
            data['lessons'].append(lesson)
    return data