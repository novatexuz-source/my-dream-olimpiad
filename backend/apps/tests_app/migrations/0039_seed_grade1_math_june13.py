# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Matematika 1-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Bir qatorda bir nechta bola turibdi. Samandar oldindan hisoblasa 4-o'rinda, orqasidan hisoblasa ham 4-o'rinda turibdi. Qatorda jami nechta bola bor?", "8", "7", "6", "9", "B"),
    (2, "Ikki xonali eng kichik juft son bilan bir xonali eng kichik toq sonning yig'indisini toping.", "11", "10", "12", "13", "A"),
    (3, "Uzunligi 10 metr bo'lgan g'o'lani 2 metrlik bo'laklarga ajratish uchun uni necha joyidan kesish kerak?", "5", "4", "3", "6", "B"),
    (4, "Qutida 2 ta ko'k va 3 ta qizil qalam bor. Qutiga qaramasdan, kamida bitta qizil qalam olish uchun eng kamida nechta qalam sug'urib olish kerak?", "3", "4", "2", "5", "A"),
    (5, "Stol ustida 3 ta butun olma va 2 ta yarimta olma bor. Stol ustida jami nechta olma bor deb hisoblash mumkin?", "5", "4", "6", "3", "B"),
    (6, "Bir uydagi 4 ta aka-ukaning har birining bittadan egizak singlisi bor. Shu oilada jami nechta farzand bor?", "8", "5", "6", "7", "B"),
    (7, "Agar 2 yil oldin Malika 5 yoshda bo'lgan bo'lsa, 3 yildan keyin u necha yoshga to'ladi?", "8", "9", "10", "7", "C"),
    (8, "3 ta mushuk 3 minutda 3 ta sichqonni tutsa, 5 ta mushuk 5 minutda nechta sichqonni tutadi?", "5", "3", "15", "25", "A"),
    (9, "Matematik qonuniyatni toping va so'roq belgisi o'rniga mos sonni qo'ying: 1, 2, 4, 7, 11, ?", "15", "16", "14", "17", "B"),
    (10, "Velosipedning 3 ta g'ildiragi bor. Mashinaning esa 4 ta g'ildiragi bor. 2 ta velosiped va 2 ta mashinaning g'ildiraklari jami nechta bo'ladi?", "12", "14", "16", "10", "B"),
    (11, "To'g'ri to'rtburchak shaklidagi qog'ozning bitta burchagi to'g'ri chiziq bo'ylab kesib tashlansa, unda nechta burchak hosil bo'ladi?", "3", "4", "5", "6", "C"),
    (12, "Sardorda 12 ta yong'oq bor edi. U ukasiga yong'oqlarining yarmini berdi, keyin singlisiga qolgan yong'oqlarning yarmini berdi. Sardorda nechta yong'oq qoldi?", "6", "4", "3", "2", "C"),
    (13, "Agar bugun shanba bo'lsa, 9 kundan keyin haftaning qaysi kuni bo'ladi?", "Yakshanba", "Dushanba", "Seshanba", "Chorshanba", "C"),
    (14, "Shunday ikki xonali eng kichik sonni topingki, uning raqamlari yig'indisi 9 ga teng bo'lsin.", "18", "90", "27", "45", "A"),
    (15, "Nargiza kitobning 5-sahifasidan 12-sahifasigacha o'qidi (5 va 12 ham kiradi). U jami nechta sahifa o'qigan?", "7", "8", "9", "6", "B"),
    (16, "Tarozi pallalarining birida 3 ta bir xil g'isht, ikkinchisida esa 1 ta xuddi shunday g'isht va 4 kg lik tosh turibdi. Tarozi muvozanatda bo'lsa, 1 ta g'ishtning vazni necha kg?", "1 kg", "2 kg", "3 kg", "4 kg", "B"),
    (17, "3 ta ketma-ket kelgan sonning yig'indisi 6 ga teng. Ularning ko'paytmasi nechaga teng bo'ladi?", "6", "8", "0", "12", "A"),
    (18, "Chizg'ichning uzunligi 20 sm. Bu necha desimetrga (dm) teng bo'ladi?", "1 dm", "2 dm", "10 dm", "5 dm", "B"),
    (19, "Sayyoh tushgacha 4 km yo'l yurdi. Tushdan keyin esa tushgachaga qaraganda 2 km kam yo'l yurdi. U jami necha kilometr yo'l yurgan?", "6 km", "8 km", "5 km", "7 km", "A"),
    (20, "Idishda 8 litr suv bor edi. Undan avval 3 litr, keyin yana bir miqdor suv olindi va idishda 2 litr suv qoldi. Ikkinchi marta idishdan necha litr suv olingan?", "2 l", "3 l", "4 l", "5 l", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

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
        ('tests_app', '0038_seed_grade11_russian_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
