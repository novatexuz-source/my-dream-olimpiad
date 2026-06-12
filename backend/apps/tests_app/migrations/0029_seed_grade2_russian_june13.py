# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Rus tili 2-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# options: А→option_a, Б→option_b, В→option_c, Г→option_d
# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "В каком слове ВСЕ согласные звуки являются МЯГКИМИ?", "Ученик", "Чаща", "Щука", "Лампа", "B"),
    (2, "Найди слово, в котором букв БОЛЬШЕ, чем звуков:", "Ягода", "Коньки", "Поезд", "Дерево", "B"),
    (3, "В каком слове буква «Ё» обозначает ДВА звука?", "Клён", "Повёл", "Ёжик", "Пёс", "C"),
    (4, "Выбери слово, в котором пропущена буква «О» (проверь однокоренным словом):", "Тр...ва", "Кр...ты", "С...ды", "Цв...ты", "B"),
    (5, "Какое слово ПРАВИЛЬНО разделено для переноса?", "Ко-нЬки", "Оля", "Класс-ная", "Маш-ина", "C"),
    (6, "Укажи слово, в котором пишется разделительный мягкий знак (Ь):", "Пал...то", "В...юга", "Мал...чик", "Пис...мо", "B"),
    (7, "В каком слове на конце нужно писать букву «В», а не «Ф»?", "Шар...", "Остро...", "Жира...", "Гра...", "B"),
    (8, "Найди пару слов, которые являются СИНОНИМАМИ (yaqin ma'noli so'zlar):", "Большой — маленький", "Алфавит — азбука", "Бежать — стоять", "Быстрый — тихий", "B"),
    (9, "Какое из этих слов является ГЛАГОЛОМ (fe'l)?", "Прыжок", "Прыгать", "Прыгучий", "Прыганье", "B"),
    (10, "Укажи имя существительное ОДУШЕВЛЁННОЕ (shaxs yoki hayvonni ifodalovchi ot):", "Робот", "Кукла", "Медведь", "Игрушка", "C"),
    (11, "В каком слове ударение падает на ТРЕТИЙ слог?", "Магазин", "Алфавит", "Воробей", "Яблоко", "C"),
    (12, "Какое слово является лишним в этом ряду родственных слов?", "Гора", "Горный", "Гореть", "Горка", "C"),
    (13, "Разгадай анаграмму. Переставь буквы: О, Л, Х, О, Д.", "Дохло", "Холод", "Лоход", "Дохол", "B"),
    (14, "Сколько звуков [ш] в предложении: «Шли сорок мышей, несли сорок грошей»?", "2", "3", "4", "5", "C"),
    (15, "Какое слово пишется с большой буквы ТОЛЬКО тогда, когда является именем собственным?", "Волга", "Орёл", "Ташкент", "Москва", "B"),
    (16, "Какое сочетание букв всегда пишется БЕЗ мягкого знака?", "ЧН", "ЛЬ", "СЬ", "ЖЬ", "A"),
    (17, "Закончи известную пословицу: «Встречают по одёжке, а провожают по...»", "Уму", "Делам", "Сёстрам", "Знаниям", "A"),
    (18, "В каком слове есть непроизносимая согласная (yozilsa ham aytilmaydigan undosh)?", "Вкусный", "Солнце", "Опасный", "Красный", "B"),
    (19, "Что нужно поставить в конце предложения: «Обязательно выучи это правило»?", "Вопросительный знак (?)", "Точку (.) или восклицательный знак (!)", "Запятую (,)", "Многоточие (...)", "B"),
    (20, "У какого слова нет формы единственного числа? (Faqat ko'plikda ishlatiladi):", "Книги", "Ножницы", "Карандаши", "Цветы", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Rus tili', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=2, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=2,
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
    Test.objects.filter(title=TITLE, grade=2).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0028_seed_grade1_russian_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
