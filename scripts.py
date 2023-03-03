import random

from datacenter.models import (Schoolkid,
                               Lesson,
                               Chastisement,
                               Commendation,
                               Mark)


COMMENDATION = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
                'Великолепно!',
                'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
                'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
                'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!',
                'Замечательно!',
                'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!', 'Это как раз то, что нужно!',
                'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!',
                'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу! ',
                'Теперь у тебя точно все получится!']


def check_scholar(scholar_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=scholar_name)
        return schoolkid
    except Schoolkid.DoesNotExist:
        print('такого ученика не существует, введите правильное имя')
        return
    except Schoolkid.MultipleObjectsReturned:
        print('с такими данными много учеников, уточните ФИО')
        return


def fix_marks(scholar_name):
    schoolkid = check_scholar(scholar_name)
    if schoolkid:
        Mark.objects.filter(points__in=(2, 3), schoolkid=schoolkid).update(points=random.choice((4, 5)))


def remove_chastisements(scholar_name):
    schoolkid = check_scholar(scholar_name)
    if schoolkid:
        Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(scholar_name, subject):
    text = random.choice(COMMENDATION)
    schoolkid = check_scholar(scholar_name)
    if schoolkid:
        lesson = Lesson.objects.filter(subject__title=subject, year_of_study=schoolkid.year_of_study,
                                       group_letter=schoolkid.group_letter).order_by('?').last()
        if not lesson:
            print(
                f'уроков с таким предметом для {schoolkid.year_of_study} класса не существует, уточните название '
                f'предмета')
            return
        Commendation.objects.create(text=text, created=lesson.date, schoolkid=schoolkid, subject=lesson.subject,
                                    teacher=lesson.teacher)
