# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Matematika 10-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Ko'rsatkichli tenglamani yeching va uning barcha haqiqiy ildizlari yig'indisini toping: 4^X - 6·2^X + 8 = 0", "3", "2", "4", "1", "A"),
    (2, "Logarifmik tenglamaning barcha haqiqiy ildizlari ko'paytmasini toping: log₃²(X) - 3·log₃(X) + 2 = 0", "27", "9", "12", "6", "A"),
    (3, "Funksiyaning hosilasini toping va uning X = 1 nuqtadagi qiymatini hisoblang: F(X) = (2X - 1) / (X + 1)", "3/4", "1/2", "1", "3/2", "A"),
    (4, "sin(2X) - cos(X) = 0 trigonometrik tenglamaning [0; π] kesmadagi barcha ildizlari yig'indisini toping.", "7π/6", "π", "π/2", "3π/2", "D"),
    (5, "cos(X) = -1/2 trigonometrik tenglamaning eng kichik musbat ildizini toping.", "2π/3", "π/3", "4π/3", "5π/6", "A"),
    (6, "Logarifmik tengsizlikni yeching va uning to'g'ri yechimlar oralig'ini ko'rsating: log₀.₅(2X - 4) ≥ -1", "(2; 3]", "[2; 3)", "(2; 4]", "(2; +∞)", "A"),
    (7, "F(X) = X³ - 6X² + 9X - 4 funksiyaning lokal maksimum nuqtasini toping.", "X = 1", "X = 3", "X = 0", "X = 2", "A"),
    (8, "Konusning to'la sirti yuzi 24π sm² ga teng. Agar uning asosi radiusi 3 sm bo'lsa, konusning hajmini toping.", "12π sm³", "15π sm³", "36π sm³", "9π sm³", "A"),
    (9, "Sfera sirtining yuzi 64π sm² ga teng. Ushbu sferaga tegishli shar hajmini toping.", "256π/3 sm³", "32π sm³", "64π sm³", "128π/3 sm³", "A"),
    (10, "Fazoda uchlari A(1; 2; 3), B(3; 2; 1) va C(1; 4; 1) nuqtalarda bo'lgan uchburchakning yuzini toping.", "2√3", "4", "4√2", "6", "A"),
    (11, "Ko'rsatkichli tengsizlikni yeching: (1/3)^(X² - 3) > 9^(-X)", "(-1; 3)", "(-∞; -1) ∪ (3; +∞)", "(-3; 1)", "(1; 3)", "A"),
    (12, "√3·sin(X) - cos(X) = 0 trigonometrik tenglamaning umumiy yechimini ko'rsating.", "X = π/6 + πK, K ∈ Z", "X = π/3 + πK, K ∈ Z", "X = -π/6 + πK, K ∈ Z", "X = π/4 + πK, K ∈ Z", "A"),
    (13, "Muntazam to'rtburchakli piramidaning asosi tomoni 6 sm ga, yon qirrasi esa 5 sm ga teng. Piramidaning hajmini toping.", "12√7 sm³", "36 sm³", "48 sm³", "24√7 sm³", "A"),
    (14, "Tenglamani yeching va uning haqiqiy ildizini aniqlang: √(X² - 3X + 2) = X - 1", "X = 1", "X = 2", "X = 1 va X = 2", "Ildizi yo'q", "A"),
    (15, "log_X(3X² - 2X) = 2 tenglamaning barcha haqiqiy ildizlari to'plamini ko'rsating.", "X = 1", "Ildizi yo'q", "X = 2", "X = 0", "B"),
    (16, "Funksiyaning monoton kamayish oralig'ini hosila yordamida toping: Y = X³/3 - 2X² + 3X", "[1; 3]", "(-∞; 1] ∪ [3; +∞)", "[0; 3]", "[1; +∞)", "A"),
    (17, "Silindr asosi radiusi 2 marta oshirilib, balandligi 4 marta kamaytirildi. Silindrning hajmi dastlabki holatga nisbatan qanday o'zgardi?", "O'zgarmadi", "2 marta ortdi", "2 marta kamaydi", "4 marta ortdi", "A"),
    (18, "Trigonometrik ifodani fundamental ayniyatlar yordamida soddalashtiring: cos²α + cos²α·cot²α", "cot²α", "tan²α", "1", "sin²α", "A"),
    (19, "Nishonga o'q uzilganda tegish ehtimolligi 0.8 ga teng. 3 marta ketma-ket o'q uzilganda nishonga kamida bir marta tegish ehtimolligini toping.", "0.992", "0.512", "0.960", "0.800", "A"),
    (20, "Fazoda berilgan A(1; -2; 2) va B(2; 1; -2) vektorlar orasidagi burchak kosinusini toping.", "-4/9", "4/9", "0", "-2/9", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=10, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=10,
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
    Test.objects.filter(title=TITLE, grade=10).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0046_seed_grade8_math_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
