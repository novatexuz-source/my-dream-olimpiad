# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Matematika 7-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Chiziqli tenglamalar sistemasini yeching va X² - Y² ifodaning aniq qiymatini toping: { 3X + 2Y = 12; 5X - 3Y = 1 }", "-5", "5", "3", "-3", "A"),
    (2, "Ifodani qisqa ko'paytirish formulalari yordamida eng sodda ko'rinishga keltiring: (2A - 3B)² - (2A + 3B)(2A - 3B) + 12AB", "18B²", "9B²", "0", "-18B²", "A"),
    (3, "Algebraik kasrni qisqartiring va uning ratsional ko'rinishini aniqlang: (A³ - 8) / (A² + 2A + 4)", "A - 2", "A + 2", "A² - 2", "A² + 2", "A"),
    (4, "X² - 7X + 10 = 0 tenglamaning ildizlari X₁ va X₂ bo'lsa, ularning kvadratlari yig'indisini (X₁² + X₂²) hisoblang.", "29", "39", "25", "34", "A"),
    (5, "Chiziqli funksiya grafigi A(2; 1) va B(-1; -5) nuqtalardan o'tadi. Y = KX + B tenglamasidagi K × B ko'paytmaning qiymatini toping.", "-6", "6", "-1", "5", "A"),
    (6, "Ikki parallel to'g'ri chiziqni uchinchi to'g'ri chiziq kesib o'tganda hosil bo'lgan ichki bir tomonli burchaklardan birining 25% i ikkinchisining 1/3 qismiga teng. Shu burchaklardan kattasini toping.", "105°", "120°", "100°", "135°", "A"),
    (7, "Uchburchakning bitta tashqi burchagi 130° ga, unga qo'shni bo'lmagan ichki burchaklarining nisbati esa 2:3 kabi. Uchburchakning eng katta ichki burchagini toping.", "78°", "52°", "50°", "60°", "A"),
    (8, "Darajali ifodani faqat musbat ko'rsatkichlar yordamida soddalashtiring: (A^(-3) × B²)^(-2) / (A² × B^(-1))³", "1/B", "A²B", "B", "1/(A²B²)", "A"),
    (9, "Teng yonli uchburchakning asosidagi burchagi uchidagi burchagidan 4 marta katta. Uchburchakning asosidagi burchaklaridan biri necha gradusga teng?", "80°", "40°", "20°", "70°", "A"),
    (10, "A⁴ + 4 to'rtinchi darajali ko'phadni ko'paytuvchilarga ajratishning to'g'ri shaklini ko'rsating.", "(A² - 2A + 2)(A² + 2A + 2)", "(A² - 2)²", "(A² + 2)²", "(A² - 2A - 2)(A² + 2A - 2)", "A"),
    (11, "To'g'ri to'rtburchakning bo'yi 25% ga orttirildi. Uning yuzi o'zgarmay qolishi uchun enini necha foizga kamaytirish kerak?", "20%", "25%", "15%", "30%", "A"),
    (12, "X³ - 5X² + 6X = 0 tenglamaning barcha haqiqiy ildizlari ko'paytmasini toping.", "0", "6", "5", "12", "A"),
    (13, "Koordinatalar tekisligida A(2; -3) nuqta koordinata boshiga nisbatan simmetrik ko'chirilgandan so'ng, hosil bo'lgan yangi nuqta Oy o'qiga nisbatan simmetrik ko'chirildi. Yakuniy nuqta koordinatasini toping.", "(2; 3)", "(-2; 3)", "(-2; -3)", "(2; -3)", "A"),
    (14, "Uchburchakning ikki tomoni 6 sm va 8 sm bo'lsa, uning perimetri qabul qilishi mumkin bo'lgan eng katta butun qiymatni toping.", "27 sm", "28 sm", "26 sm", "25 sm", "A"),
    (15, "Ko'phadni qisqa ko'paytirish formulalari yordamida soddalashtiring: (X + 1)(X² - X + 1) - (X - 1)(X² + X + 1)", "2", "2X³", "0", "-2", "A"),
    (16, "Funksiya Y = (2X - 1) / 3 formula bilan berilgan. Y = X - 3 bo'ladigan argument X ning qiymatini toping.", "8", "7", "6", "9", "A"),
    (17, "Aylana tashqarisidagi nuqtadan aylanaga ikkita urinma o'tkazilgan. Urinmalar orasidagi burchak 60° bo'lsa, urinish nuqtalari aylanani ajratgan yoylardan kattasining qiymatini toping.", "240°", "120°", "180°", "300°", "A"),
    (18, "Chiziqli tenglamalar sistemasi cheksiz ko'p yechimga ega bo'ladigan A va B parametrlarning yig'indisini (A+B) toping: { AX + 2Y = 4; 3X + 4Y = B }", "9.5", "10", "8.5", "11", "A"),
    (19, "Agar A + B + C = 0 bo'lsa, A³ + B³ + C³ ifoda quyidagilardan qaysi biriga har doim teng bo'ladi?", "3ABC", "0", "-3ABC", "A³B³C³", "A"),
    (20, "To'g'ri to'rtburchak diagonallarining kesishish burchaklaridan biri 60° ga teng. Kichik tomoni va diagonalining yig'indisi 15 sm bo'lsa, diagonalning uzunligini toping.", "10 sm", "5√3 sm", "6 sm", "8 sm", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=7, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=7,
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
    Test.objects.filter(title=TITLE, grade=7).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0044_seed_grade6_math_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
