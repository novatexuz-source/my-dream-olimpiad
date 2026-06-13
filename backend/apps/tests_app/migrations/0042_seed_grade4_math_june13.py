# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Matematika 4-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "A, B, C har xil raqamlar bo'lib, uch xonali ABC + uch xonali BCA + uch xonali CAB = 1998 bo'lsa (bu yerda ABC, BCA, CAB uch xonali sonlar), A + B + C yig'indisining qiymati nechaga teng bo'ladi?", "18", "9", "27", "12", "A"),
    (2, "Kvadratning ichiga uning hamma tomonlariga tegib turadigan aylana chizildi. Agar kvadratning perimetri 48 sm bo'lsa, aylananing radiusi necha sm bo'ladi?", "6 sm", "12 sm", "3 sm", "4 sm", "A"),
    (3, "Avtomobil shaharlararo masofaning birinchi yarmini 60 km/h tezlik bilan, ikkinchi yarmini esa 90 km/h tezlik bilan bosib o'tdi. Avtomobilning butun yo'ldagi o'rtacha tezligini (km/h) toping.", "75 km/h", "72 km/h", "70 km/h", "80 km/h", "B"),
    (4, "Idishda 12 litr sut bor edi. Uni ikki kishi 6 litrdan qilib teng bo'lishmoqchi. Ularda faqat 5 litrlik va 8 litrlik bo'sh idishlar bor. Bu ishni eng kamida necha marta quyish amali bilan bajarish mumkin?", "7 marta", "6 marta", "5 marta", "8 marta", "A"),
    (5, "Quyidagi ko'paytmaning oxirida nechta nol raqami bor: 1 × 2 × 3 × 4 × ... × 25?", "4 ta", "5 ta", "6 ta", "3 ta", "C"),
    (6, "Tenglamani yeching va X ning qiymatini toping: 1200 ÷ [450 - (15 × X + 30)] = 4", "10", "8", "12", "6", "B"),
    (7, "To'g'ri to'rtburchak shaklidagi maydonning bo'yi enidan 20 metr uzun. Maydonning atrofi bo'ylab uzunligi 4 metr bo'lgan jami 60 ta panel panjara o'rnatib chiqildi. Maydonning yuzini toping.", "3500 m²", "2400 m²", "3000 m²", "4000 m²", "A"),
    (8, "Samandar kitobning uchdan bir (1/3) qismini o'qidi. Agar u yana 40 sahifa o'qisa, kitobning yarmi (1/2) o'qilgan bo'lar edi. Kitob jami necha sahifadan iborat?", "240 sahifa", "120 sahifa", "180 sahifa", "300 sahifa", "A"),
    (9, "X/24 kasr to'g'ri kasr bo'lsa va uni qisqartirib bo'lmasa, X o'rniga qo'yish mumkin bo'lgan natural sonlar nechta?", "8 ta", "10 ta", "7 ta", "9 ta", "A"),
    (10, "Sinfda 28 ta o'quvchi bor. Ulardan 15 tasi matematika to'garagiga, 14 tasi fizika to'garagiga qatnashadi. 5 ta o'quvchi esa ikkala to'garakka ham qatnashmaydi. Nechta o'quvchi faqat matematika to'garagiga qatnashadi?", "9 ta", "6 ta", "10 ta", "11 ta", "A"),
    (11, "Hozir ona 38 yoshda, uning o'g'illari esa 12 va 8 yoshda. Necha yildan keyin onasining yoshi ikki o'g'li yoshlarining yig'indisiga teng bo'ladi?", "18 yildan keyin", "16 yildan keyin", "20 yildan keyin", "14 yildan keyin", "A"),
    (12, "Ikki sonning yig'indisi 121 ga teng. Agar ulardan birining oxiridagi 0 raqami o'chirilsa, ikkinchi son hosil bo'ladi. Shu sonlardan kattasining qiymatini toping.", "100", "110", "120", "90", "B"),
    (13, "Tomoni 6 sm bo'lgan kub shaklidagi yog'och blokning tashqi sirti butunlay qizil rangga boyaldi. Keyin u tomoni 1 sm bo'lgan kichik kubchalarga kesib chiqildi. Hosil bo'lgan kubchalarning nechtasining faqat ikkita tomoni qizil rangli bo'ladi?", "48 ta", "36 ta", "24 ta", "54 ta", "A"),
    (14, "Soat mili 1 soatda 30° ga buriladi. 3 soat 20 minut davomida soat mili jami necha gradusga buriladi?", "100°", "95°", "105°", "110°", "A"),
    (15, "Do'konda 3 ta daftar, 2 ta ruchka va 1 ta chizg'ich jami 3200 so'm turadi. 1 ta daftar, 2 ta ruchka va 3 ta chizg'ich esa 2400 so'm tursa, 1 ta daftar, 1 ta ruchka va 1 ta chizg'ich birgalikda qancha turadi?", "1400 so'm", "1500 so'm", "1600 so'm", "1200 so'm", "A"),
    (16, "To'g'ri to'rtburchakning bo'yi 20% ga oshirildi, eni esa 20% ga kamaytirildi. To'rtburchakning yuzi qanday o'zgardi?", "O'zgarmadi", "4% ga kamaydi", "4% ga ortdi", "2% ga kamaydi", "B"),
    (17, "Qutida 1 dan 20 gacha bo'lgan sonlar yozilgan 20 ta kartochka bor. Qutiga qaramay ichidan olingan kartochkadagi sonning tub son bo'lish ehtimolligini toping.", "2/5", "1/2", "3/10", "7/20", "A"),
    (18, "Uzunligi 120 metr bo'lgan poyezd svetofor ustuni yonidan 6 sekundda o'tib ketdi. Xuddi shu poyezd uzunligi 400 metr bo'lgan tunneldan jami necha sekundda to'liq o'tib ketadi?", "20 sekund", "26 sekund", "24 sekund", "22 sekund", "B"),
    (19, "Raqamlari har xil bo'lgan eng katta to'rt xonali juft sonni ko'rsating.", "9876", "9998", "9874", "9864", "A"),
    (20, "1 dan 100 gacha bo'lgan sonlar (100 ham kiradi) ketma-ket yozib chiqilganda 9 raqami jami necha marta ishlatiladi?", "19 marta", "20 marta", "10 marta", "11 marta", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=4, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=4,
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
    Test.objects.filter(title=TITLE, grade=4).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0041_seed_grade3_math_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
