# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Rus tili 5-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# options: А→option_a, Б→option_b, В→option_c, Г→option_d
# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "В каком ряду во всех словах букв БОЛЬШЕ, чем звуков?", "Солнце, честность, июнь", "Ягода, ёлка, вьюга", "Поезд, местность, класс", "Лес, дом, кот", "A"),
    (2, "Укажи слово, в котором все согласные звуки — ГЛУХИЕ (jarangsiz):", "Петух", "Салат", "Коса", "Задача", "A"),
    (3, "В каком слове на месте пропуска пишется буква «И»?", "Ц...ган", "Ц...рк", "Спиц...", "Огурц...", "B"),
    (4, "В каком варианте во всех словах пишется буква «О» после шипящих под ударением в корне?", "Шёлк, чёрный, жёлтый", "Шов, крыжовник, капюшон", "Щёчка, пчела, шоколад", "Шёрсть, жёсткий, чёткий", "B"),
    (5, "Найди слово с чередующейся гласной в корне (o'zagi o'zgaradigan so'z):", "Вода", "Растение", "Трава", "Земля", "B"),
    (6, "Какое из этих слов является НЕИЗМЕНЯЕМЫМ существительным (kelishiklarda o'zgarmaydigan ot)?", "Пальто", "Окно", "Стол", "Книга", "A"),
    (7, "Укажи существительное, которое имеет форму ТОЛЬКО единственного числа:", "Вода", "Золото", "Книга", "Тетрадь", "B"),
    (8, "В каком слове на конце после шипящего НЕ ПИШЕТСЯ мягкий знак (Ь)?", "Береч...", "Плащ...", "Мыш...", "Ноч...", "B"),
    (9, "Укажи глагол-исключение, который относится к II спряжению:", "Брить", "Стелить", "Дышать", "Читать", "C"),
    (10, "В каком варианте «НЕ» с глаголом пишется СЛИТНО (birga)?", "(Не)навидеть", "(Не)хотеть", "(Не)знать", "(Не)думать", "A"),
    (11, "Какое прилагательное является КАЧЕСТВЕННЫМ (darajaga ega bo'la oladigan)?", "Деревянный стол", "Умный мальчик", "Лисий хвост", "Берёзовая роща", "B"),
    (12, "Какое местоимение является ОТРИЦАТЕЛЬНЫМ (bo'lishsizlik olmoshi)?", "Никто", "Кто-то", "Себя", "Некто", "A"),
    (13, "Определи разряд числительного «ПЯТЫЙ»:", "Количественное (miqdor)", "Порядковое (tartib)", "Собирательное (jamlovchi)", "Дробное (kasr)", "B"),
    (14, "Какое из слов является РЕЧЕВОЙ ОШИБКОЙ (плеоназм — ortiqcha so'z qo'llangan)?", "Старый старик", "Пожилой человек", "Древний город", "Высокий дом", "A"),
    (15, "В каком предложении знак препинания (пунктуация) поставлен НЕВЕРНО?", "Я люблю читать книги, рисовать и плавать.", "Ребята, вы готовы к уроку?", "Ветер дул и, деревья гнулись.", "Солнце светит, и дети играют на улице.", "C"),
    (16, "Определи синтаксическую роль выделенного слова: «Мы приехали в Ташкент».", "Дополнение (to'ldiruvchi)", "Обстоятельство (hol)", "Подлежащее (ega)", "Определение (aniqlovchi)", "B"),
    (17, "В каком слове пишется приставка ПРИ-?", "Пр...красный", "Пр...ехать", "Пр...мудрый", "Пр...ступление", "B"),
    (18, "Какой частью речи является выделенное слово: «В классе было тихо»?", "Имя прилагательное", "Наречие (или категория состояния)", "Глагол", "Союз", "B"),
    (19, "Найди слово с РАЗДЕЛИТЕЛЬНЫМ ТВЁРДЫМ знаком (Ъ):", "С...экономить", "Об...явление", "Мурав...и", "Стат...я", "B"),
    (20, "Укажи слово, в котором суффикс служит для образования формы прошедшего времени глагола:", "Писал", "Писать", "Пишу", "Пишет", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Rus tili', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=5, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=5,
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
    Test.objects.filter(title=TITLE, grade=5).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0031_seed_grade4_russian_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
