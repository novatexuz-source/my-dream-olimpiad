# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Matematika 6-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Kasrli chiziqli tenglamani yeching va X ning qiymatini toping: (3X - 2)/4 - (2X + 1)/3 = (X - 3)/6", "X = 4", "X = 2", "X = -4", "X = 1", "C"),
    (2, "A va B natural sonlarining ko'paytmasi 1200 ga, ularning Eng Kichik Umumiy Karralisi (EKUK) esa 240 ga teng. Shu sonlarning Eng Katta Umumiy Bo'luvchisini (EKUB) toping.", "5", "10", "12", "15", "A"),
    (3, "Uchta ketma-ket kelgan tub sonlarning ko'paytmasi 1001 ga teng. Shu sonlarning yig'indisini toping.", "31", "29", "33", "35", "A"),
    (4, "200 gramm 30% li shakar eritmasiga necha gramm toza shakar qo'shilsa, uning konsentratsiyasi (shakar miqdori) 44% ga ko'tariladi?", "50 g", "40 g", "60 g", "30 g", "A"),
    (5, "Koordinatalari A(-2; 5) va B(4; -3) bo'lgan nuqtalar berilgan. AB kesma o'rtasining koordinatalarini va shu kesmaning uzunligini toping.", "(1; 1) va 10", "(1; 1) va 5", "(-1; 1) va 10", "(1; -1) va 8", "A"),
    (6, "Ifodani oching va o'xshash hadlarni ixchamlang: -2(3X - 4Y) + 3(2X - 5Z) - 4(2Y - 3Z)", "-3Z", "8Y - 3Z", "6X - 3Z", "16Y - 27Z", "A"),
    (7, "120 sonining 5/6 qismidan qaysi sonning 40% ini ayirganda 64 soni hosil bo'ladi?", "90", "80", "100", "75", "A"),
    (8, "Aylana ichiga chizilgan muntazam oltiburchakning perimetri 36 sm. Shu aylananing uzunligini toping (π ≈ 3.14).", "37.68 sm", "18.84 sm", "75.36 sm", "50.24 sm", "A"),
    (9, "6 ta sonning o'rta arifmetigi 15 ga teng. Shu sonlardan bittasi chiqarib tashlangandan keyin, qolgan sonlarning o'rta arifmetigi 17 ga teng bo'lib qoldi. Chiqarib tashlangan sonni toping.", "5", "7", "9", "6", "A"),
    (10, "Murakkab proporsiyadan noma'lum X hadni toping: (1.2X - 0.8) / 2.5 = 3.2 / 2", "4", "3.6", "3.2", "2.8", "A"),
    (11, "To'g'ri burchakli uchburchakning o'tkir burchaklari ayirmasi 24° ga teng. Shu uchburchakning katta o'tkir burchagini toping.", "57°", "66°", "54°", "60°", "A"),
    (12, "Tekislikda 7 ta nuqta belgilandi, ulardan hech qaysi uchtasi bir to'g'ri chiziqda yotmaydi. Bu nuqtalar orqali jami nechta har xil to'g'ri chiziq o'tkazish mumkin?", "21 ta", "14 ta", "28 ta", "15 ta", "A"),
    (13, "-4X + 7 ≥ -13 tengsizlikning barcha natural yechimlari yig'indisini toping.", "15", "10", "21", "12", "A"),
    (14, "Sexda erkaklar sonining ayollar soniga nisbati 5:3 kabi. Sexga yana 6 ta ayol ishga olingandan keyin bu nisbat 1:1 bo'lib qoldi. Dastlab sexda jami nechta ishchi bo'lgan?", "24 ta", "16 ta", "32 ta", "40 ta", "A"),
    (15, "O'ylangan sonning 45% idan 14 ayirilsa, natija shu sonning uchdan bir (1/3) qismiga teng bo'ladi. O'ylangan sonni toping.", "120", "90", "100", "150", "A"),
    (16, "Modulli ifodani hisoblang: (|-4.5| × |-2| - |-3.6| ÷ 0.6) / (|-1.5| - |+0.5|)", "3", "1.5", "4.5", "2", "A"),
    (17, "Berilgan davriy o'nli kasrni oddiy kasr shaklida ifodalang: 0.2(3)", "7/30", "23/99", "1/3", "7/33", "A"),
    (18, "Ikki shahar orasidagi masofa haqiqatda 45 km. 1:300 000 miqyosli (masshtabli) xaritada shu masofa necha sm kesma bilan tasvirlanadi?", "15 sm", "12 sm", "10 sm", "20 sm", "A"),
    (19, "Idishdagi sutning 20% i ichildi, keyin esa qolgan sutning 25% i mushukka berildi. Idishda dastlabki sutning necha foizi qoldi?", "55%", "60%", "50%", "65%", "B"),
    (20, "Koordinata to'g'ri chizig'ida -5 va X sonlari orasidagi masofa 8 birlikka teng. X ning qabul qilishi mumkin bo'lgan barcha qiymatlari yig'indisini toping.", "-10", "-5", "-2", "0", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=6, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=6,
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
    Test.objects.filter(title=TITLE, grade=6).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0043_seed_grade5_math_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
