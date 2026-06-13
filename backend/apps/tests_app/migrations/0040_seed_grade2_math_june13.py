# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Matematika 2-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "A + B = 14 va A - B = 4 bo'lsa, A × B ko'paytmaning qiymati nechaga teng bo'ladi?", "40", "45", "48", "50", "B"),
    (2, "Shunday ikki xonali sonni topingki, uning o'nlar xonasidagi raqam birlar xonasidagi raqamidan 3 marta katta, raqamlar yig'indisi esa 8 dan kam bo'lsin.", "31", "62", "93", "41", "A"),
    (3, "Kvadratning perimetri 24 sm. Bo'yi shu kvadratning tomoniga teng, eni esa undan 2 sm qisqa bo'lgan to'g'ri to'rtburchakning perimetrini toping.", "20 sm", "18 sm", "16 sm", "22 sm", "A"),
    (4, "To'garakda 18 ta bola bor. Ulardan 10 tasi rasm chizishni, 12 tasi esa shaxmat o'ynashni yaxshi ko'radi. Necha kishi ikkala mashg'ulotni ham yaxshi ko'radi?", "2", "4", "6", "3", "B"),
    (5, "3 ta savatda jami 45 ta olma bor. Birinchi va ikkinchi savatda 28 ta, ikkinchi va uchinchi savatda esa 32 ta olma bo'lsa, ikkinchi savatda nechta olma bor?", "13", "15", "12", "17", "B"),
    (6, "Ustaxonada 3 g'ildirakli va 2 g'ildirakli velosipedlar yasaladi. Jami 10 ta velosiped va ularning 26 ta g'ildiragi bo'lsa, 3 g'ildirakli velosipedlar nechta?", "4", "6", "5", "3", "B"),
    (7, "Onasi 32 yoshda, qizi esa 8 yoshda. Necha yil oldin onasi qizidan 5 marta katta bo'lgan?", "2 yil oldin", "3 yil oldin", "4 yil oldin", "5 yil oldin", "A"),
    (8, "Matematik zanjirni davom ettiring: 3, 4, 7, 11, 18, 29, ... Keyingi sonni toping.", "38", "47", "42", "45", "B"),
    (9, "Idishning uchdan bir qismi (1/3) suv bilan to'ldirilganda uning vazni 5 kg chiqdi. Idish to'liq to'ldirilganda esa 11 kg chiqdi. Bo'sh idishning o'z vazni necha kg?", "1 kg", "2 kg", "3 kg", "4 kg", "B"),
    (10, "1 dan 38 gacha bo'lgan sonlar orasida (38 ham kiradi) 3 raqami jami necha marta ishlatilgan?", "11 marta", "12 marta", "13 marta", "10 marta", "C"),
    (11, "Kamol bir son o'yladi. Uni 4 marta oshirib, hosil bo'lgan natijadan 12 ni ayirganda 28 hosil bo'ldi. Kamol qaysi sonni o'ylagan?", "9", "10", "8", "11", "B"),
    (12, "4 ta ketma-ket kelgan juft sonning yig'indisi 36 ga teng. Shu sonlarning eng kichigini toping.", "4", "6", "8", "10", "B"),
    (13, "Sim bo'lagini 5 marta kesib, teng bo'laklarga ajratishdi. Har bir bo'lakning uzunligi 4 sm bo'lsa, simning dastlabki uzunligi necha sm bo'lgan?", "20 sm", "24 sm", "16 sm", "28 sm", "B"),
    (14, "Soat mili har kuni 2 minutga orqada qoladi. To'g'rilab qo'yilgan soat 10 kundan keyin necha minutga orqada qolib ketadi?", "12 minut", "20 minut", "15 minut", "25 minut", "B"),
    (15, "Bir guruh qushlar daraxtlarga qo'nmoqchi. Agar har bir daraxtga bittadan qo'nishsa, 2 ta qush joy topolmay qoladi. Agar har bir daraxtga ikkitadan qo'nishsa, 1 ta daraxt bo'sh qoladi. Qushlar nechta?", "4 ta", "6 ta", "5 ta", "8 ta", "B"),
    (16, "Kvadrat shaklidagi hovlining bitta tomoni 9 metr. Hovlining atrofiga har 3 metrda bittadan gul ko'chati ekib chiqildi (burchaklarni ham hisobga oling). Jami nechta gul ko'chati ekilgan?", "12 ta", "9 ta", "10 ta", "16 ta", "A"),
    (17, "24 ta konfetni 3 ta bolaga shunday taqsimlangki, ikkinchi bola birinchisidan 2 ta ko'p, uchinchi bola esa ikkinchisidan 2 ta ko'p konfet olsin. Birinchi bola nechta konfet olgan?", "6 ta", "8 ta", "10 ta", "4 ta", "A"),
    (18, "Yig'indisi 14 ga, ko'paytmasi esa 48 ga teng bo'lgan ikki sonning ayirmasini toping.", "2", "4", "1", "3", "A"),
    (19, "Sinfda 22 ta o'quvchi bor. Agar partalarga o'quvchilar 2 kishidan o'tirishsa, 2 ta parta mutloq bo'sh qoladi. Sinfda nechta parta bor?", "11 ta", "13 ta", "12 ta", "14 ta", "B"),
    (20, "1 ta tarvuzning vazni 2 ta qovun va 1 kg lik toshning vazniga teng. 2 ta tarvuzning vazni esa 5 ta qovunning vazniga teng bo'lsa, 1 ta qovun necha kg chiqadi?", "2 kg", "3 kg", "4 kg", "1 kg", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

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
        ('tests_app', '0039_seed_grade1_math_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
