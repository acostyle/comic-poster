import random
from datacenter.models import (Chastisement, Schoolkid, Mark, Lesson, Commendation)


def get_schoolkid_information(child_full_name):
    child = Schoolkid.objects.get(full_name__contains=child_full_name)
    
    return child


def remove_chastisements(schoolkid_information):
    all_bad_marks = Chastisement.objects.filter(schoolkid=schoolkid_information)
    for bad_mark in all_bad_marks:
        bad_mark.delete()


def change_bad_marks(schoolkid_information):
    all_bad_marks = Mark.objects.filter(schoolkid=schoolkid_information, points__lt=4)

    for bad_mark in all_bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def get_lesson_information(schoolkid_information, lesson):
    lesson_information = Lesson.objects.filter(
        group_letter=schoolkid_information.group_letter,
        year_of_study=schoolkid_information.year_of_study,
        subject__title=lesson).order_by('-date').first()
    
    return lesson_information


def get_random_commendation(commendations):
    commendation = random.choice(commendations)

    return commendation


def create_commendation(schoolkid_information, lesson_information, commendation):
    Commendation.objects.create(
        teacher=lesson_information.teacher, 
        subject=lesson_information.subject, 
        created=lesson_information.date,
        schoolkid=schoolkid_information, 
        text=commendation)



def main():
    try:
        child_full_name = input('Введите имя и фамилию ученика/ученицы: ')
        schoolkid = get_schoolkid_information(child_full_name)
    except Schoolkid.DoesNotExist:
        exit('Такого ученика/ученицы нет')
    except Schoolkid.MultipleObjectsReturned:
        exit('Слишком много учеников/учениц с таким именем')
    print('Готово')

    remove_chastisements(schoolkid)
    change_bad_marks(schoolkid)

    lesson = input('Введите название урока: ')
    lesson_information = get_lesson_information(schoolkid, lesson)

    commendations = [
        "Молодец!", "Отлично!", "Хорошо!",
        "Гораздо лучше, чем я ожидал!",
        "Ты меня приятно удивил!",
        "Великолепно!", "Прекрасно!",
        "Ты меня очень обрадовал!",
        "Именно этого я давно ждал от тебя!",
        "Сказано здорово – просто и ясно!",
        "Ты, как всегда, точен!",
        "Очень хороший ответ!", "Талантливо!",
        "Ты сегодня прыгнул выше головы!", "Я поражен!",
        "Уже существенно лучше!", "Потрясающе!",
        "Замечательно!", "Прекрасное начало!",
        "Так держать!", "Ты на верном пути!",
        "Здорово!", "Это как раз то, что нужно!", "Я тобой горжусь!",
        "С каждым разом у тебя получается всё лучше!",
        "Мы с тобой не зря поработали!", "Я вижу, как ты стараешься!",
        "Ты растешь над собой!", "Ты многое сделал, я это вижу!",
        "Теперь у тебя точно все получится!"]

    commendation = get_random_commendation(commendations)
    create_commendation(schoolkid, lesson_information, commendation)


if __name__ == '__main__':
    main()