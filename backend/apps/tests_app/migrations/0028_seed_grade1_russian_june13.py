# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Rus tili 1-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# options: А→option_a, Б→option_b, В→option_c, Г→option_d
# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "В каком слове букв больше, чем звуков? (Qaysi so'zda harf tovushdan ko'p?)", "Юбка", "Мальчик", "Ёлка", "Дом", "B"),
    (2, "В каком слове все согласные звуки — ТВЁРДЫЕ? (Qaysi so'zda hamma undoshlar qattiq?)", "Лимон", "Машина", "Чашка", "Чай", "B"),
    (3, "Найди слово, в котором буква «Е» обозначает ДВА звука:", "Река", "Лес", "Енот", "Берег", "C"),
    (4, "Выбери слово, которое ПРАВИЛЬНО разделено для переноса:", "О-сень", "Зай-ка", "Ма-льчик", "А-брикос", "B"),
    (5, "Найди ошибку в слове:", "Чаща", "Чюдо", "Жираф", "Чистый", "B"),
    (6, "Из букв слова «ТРАКТОР» можно составить слово:", "Кот", "Рот", "Ток", "Вор", "B"),
    (7, "Какое слово не имеет пары по числу? (Faqat bitta shaklda ishlatiladigan so'z):", "Брюки", "Карандаш", "Книга", "Тетрадь", "A"),
    (8, "Какое сочетание букв пишется БЕЗ мягкого знака (Ь)?", "ЧК", "ТЬ", "РЬ", "НЬ", "A"),
    (9, "Разгадай анаграмму (буквы перепутались): Р, К, И, Г, А. Что это за слово?", "Играк", "Книга", "Парик", "Крига", "B"),
    (10, "Какое слово отвечает на вопрос КТО?, но не является человеком?", "Доктор", "Собака", "Стол", "Цветок", "B"),
    (11, "Сколько слогов в слове «ЮБИЛЕЙ»?", "2", "3", "4", "5", "B"),
    (12, "Какое слово «спряталось» внутри слова «ПОДВАЛ»?", "Два", "Вол", "Вал", "Дом", "C"),
    (13, "Укажи слово, в котором ударение падает на ВТОРОЙ слог:", "Азбука", "Арбуз", "Дерево", "Облако", "B"),
    (14, "Найди лишнее слово по смыслу (bir xil o'zakli bo'lmagan so'z):", "Вода", "Водный", "Водитель", "Водоём", "C"),
    (15, "Какая из этих букв ВСЕГДА обозначает мягкий согласный звук?", "Ч", "Ш", "Ж", "Г", "A"),
    (16, "Посчитай, сколько звуков в слове «ЯМА»?", "3", "4", "2", "5", "B"),
    (17, "В каком предложении знак препинания в конце поставлен НЕВЕРНО?", "Как тебя зовут?", "Какая красивая роза!", "Кто пришёл в гости.", "Дети играют в саду.", "C"),
    (18, "Какое слово пишется с заглавной (большой) буквы, только если это имя или начало предложения?", "Шарик (собака)", "шарик (воздушный)", "Москва", "Воронеж", "B"),
    (19, "Закончи фразеологизм: «Голоден как ...»", "Заяц", "Волк", "Медведь", "Лиса", "B"),
    (20, "Сколько гласных ЗВУКОВ в русском языке? (Букв 10, а звуков?)", "6", "10", "5", "8", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Rus tili', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=1, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=1,
        title=TITLE,
        duration_minutes=20,
        passing_percentage=0.0,
        is_active=True,
        start_datetime=START,
        end_datetime=END,
    )

    for order, text, a, b, c, d, correct in DATA:
        Question.objects.create(
            test=test,
            order_number=order,
            question_text=text,
            option_a=a,
            option_b=b,
            option_c=c,
            option_d=d,
            correct_answer=correct,
        )


def unseed(apps, schema_editor):
    Test = apps.get_model('tests_app', 'Test')
    Test.objects.filter(title=TITLE, grade=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0027_seed_grade11_english_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
