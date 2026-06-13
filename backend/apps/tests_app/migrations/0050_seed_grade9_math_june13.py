# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Matematika 9-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "X² - 5X + 2 = 0 kvadrat tenglamaning haqiqiy ildizlari X₁ va X₂ bo'lsa, 1/X₁² + 1/X₂² ifodaning aniq qiymatini toping.", "21/4", "25/4", "21", "17/4", "A"),
    (2, "Ildiz ostidagi irratsional ifodani soddalashtiring va hisoblang: √(11 - 6√2) + √(11 + 6√2)", "6", "2√11", "3√2", "6√2", "A"),
    (3, "Ratsional kasrli ifodani qisqa ko'paytirish formulalari yordamida soddalashtiring: (A/(A-3) - A/(A+3)) × (A² - 9) / (6A)", "1", "A", "A/3", "6", "A"),
    (4, "To'g'ri burchakli uchburchakning katetlaridan biri 15 sm ga, uning gipotenuzadagi proeksiyasi esa 9 sm ga teng. Shu uchburchakning yuzini toping.", "150 sm²", "120 sm²", "200 sm²", "180 sm²", "A"),
    (5, "Parallelogrammning o'tkir burchagi 30° ga teng. Uning qo'shni tomonlari mos ravishda 8 sm va 12 sm bo'lsa, parallelogrammning yuzini hisoblang.", "48 sm²", "96 sm²", "24 sm²", "48√3 sm²", "A"),
    (6, "X⁴ - 13X² + 36 = 0 bikvadrat tenglamaning barcha haqiqiy ildizlari ko'paytmasini toping.", "36", "-36", "6", "-6", "A"),
    (7, "Rombning perimetri 40 sm ga va diagonallaridan biri 12 sm ga teng bo'lsa, uning yuzini aniqlang.", "96 sm²", "192 sm²", "48 sm²", "120 sm²", "A"),
    (8, "Teng yonli trapetsiyaning asoslari 10 sm va 22 sm ga, yon tomoni esa 10 sm ga teng. Trapetsiyaning yuzini toping.", "128 sm²", "96 sm²", "160 sm²", "144 sm²", "A"),
    (9, "Quyidagi tengsizliklar sistemasining barcha butun yechimlari yig'indisini hisoblang: { (2X - 5)/3 > 1; 4X - 3 ≤ 21 }", "15", "11", "9", "14", "B"),
    (10, "√(2X + 5) - √(X - 1) = 2 irratsional tenglamaning barcha haqiqiy ildizlari yig'indisini toping.", "12", "2", "10", "8", "A"),
    (11, "To'g'ri to'rtburchakning perimetri 34 sm ga va diagonali 13 sm ga teng. To'rtburchakning yuzini toping.", "60 sm²", "120 sm²", "48 sm²", "72 sm²", "A"),
    (12, "Y = -X² + 6X - 5 kvadrat funksiyaning (parabolaning) eng katta qiymatini (ekstremumini) toping.", "4", "3", "5", "9", "A"),
    (13, "Har bir ichki burchagi 144° bo'lgan muntazam ko'pburchakning nechta tomoni bor?", "10", "12", "8", "15", "A"),
    (14, "X² - (A+3)X + 2A + 5 = 0 tenglamaning ildizlaridan biri 3 ga teng bo'lsa, A parametrning qiymatini toping.", "5", "-5", "4", "-4", "A"),
    (15, "Rombning o'tkir burchagi 45° ga, uning qarshisidagi balandligi esa 6 sm ga teng. Rombning perimetrini toping.", "24√2 sm", "24 sm", "12√2 sm", "48 sm", "A"),
    (16, "Uchburchakning o'rta chizig'i uning parallel asosidan 5 sm ga qisqa. Shu o'rta chiziq va asos uzunliklarining yig'indisini toping.", "15 sm", "10 sm", "20 sm", "25 sm", "A"),
    (17, "Ratsional ifodani qisqa ko'paytirish formulalari yordamida ixchamlang: (A³ - B³) / (A - B) - 3AB", "(A - B)²", "A² + B²", "(A + B)²", "A² - B²", "A"),
    (18, "Murakkab kvadrat ildiz formulasidan foydalanib ifodani soddalashtiring: √(7 - 4√3)", "2 - √3", "√3 - 2", "2 + √3", "4 - √3", "A"),
    (19, "Parallelogrammning tomonlari 7 sm va 9 sm ga, diagonallaridan biri esa 8 sm ga teng. Uning ikkinchi diagonalining uzunligini toping.", "14 sm", "12 sm", "10 sm", "16 sm", "A"),
    (20, "A parametrning qanday eng kichik butun qiymatida X² - 4X + A = 0 kvadrat tenglama haqiqiy ildizga ega bo'lmaydi?", "5", "4", "3", "6", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=9, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=9,
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
    Test.objects.filter(title=TITLE, grade=9).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0049_seed_grade10_math_master_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
