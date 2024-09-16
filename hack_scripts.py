from datacenter.models import Mark, Commendation, Chastisement, Schoolkid, Lesson
from random import choice

COMMENDATIONS = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!'
]


def get_schoolkid():
    name = input('Введите ФИО ученика: ')
    try:
        return Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.MultipleObjectsReturned:
        raise ValueError('Пожалуйста, уточните запрос. Найдено несколько учеников.')
    except Schoolkid.DoesNotExist:
        raise ValueError('Этот ученик не найден. Пожалуйста, проверьте правильность запроса.')


def fix_marks():
    schoolkid = get_schoolkid()
    if schoolkid:
        Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements():
    schoolkid = get_schoolkid()
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()
    print('Замечания удалены!')


def create_commendation():
    schoolkid = get_schoolkid()
    subject_title = input("Введите название предмета: ")
    if schoolkid:
        lessons = Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                        group_letter=schoolkid.group_letter,
                                        subject__title=subject_title)
        if not lessons:
            print("Урок не найден.")
        else:
            random_text = choice(COMMENDATIONS)
            random_lesson = lessons.order_by('?').first()
            created = random_lesson.date
            subject = random_lesson.subject
            teacher = random_lesson.teacher
            Commendation.objects.create(text=random_text,
                                        created=created,
                                        schoolkid=schoolkid,
                                        subject=subject,
                                        teacher=teacher)
            print('Похвала получена!')


if __name__ == '__main__':
    main()

