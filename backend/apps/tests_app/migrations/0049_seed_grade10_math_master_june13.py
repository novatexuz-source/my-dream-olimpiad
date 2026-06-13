# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Matematika 10-sinf Master (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Tenglamani yeching: sin⁴(x) + cos⁴(x) = 5/8", "±π/6 + πk, k∈Z", "±π/3 + πk/2, k∈Z", "±π/6 + πk/2, k∈Z", "±π/4 + πk/2, k∈Z", "C"),
    (2, "Ko'rsatkichli tenglamaning haqiqiy ildizlari yig'indisini toping: 4^x - 6·2^x + 8 = 0", "3", "2", "6", "5", "A"),
    (3, "Agar log₂3 = a bo'lsa, log₁₂18 ifodani a orqali ifodalang.", "(1 + 2a) / (2 + a)", "(1 + a) / (2 + a)", "(2 + a) / (1 + 2a)", "2a / (1 + a)", "A"),
    (4, "Kubning diagonali 6 sm ga teng. Shu kubning to'la sirti yuzini (S) toping.", "36 sm²", "72 sm²", "54 sm²", "48 sm²", "B"),
    (5, "Tenglamani yeching: √(x + 1) - √(x - 2) = 1", "x = 3", "x = 2", "x = 4", "x = 5", "A"),
    (6, "y = log₀.₅(x² - 4x + 3) funksiyaning qiymatlar sohasini (OQF) toping.", "(-∞; 0]", "[0; +∞)", "Barcha haqiqiy sonlar (R)", "(0; +∞)", "C"),
    (7, "Agar tan(x) + cot(x) = 3 bo'lsa, tan³(x) + cot³(x) ning qiymatini toping.", "18", "27", "36", "9", "A"),
    (8, "Muntazam to'rtburchakli piramidaning asosi tomoni 6 sm, balandligi esa 4 sm. Piramidaning hajmini (V) toping.", "48 sm³", "144 sm³", "36 sm³", "72 sm³", "A"),
    (9, "7 ta o'quvchidan 3 kishilik qo'mita (guruh)ni nechta usul bilan tanlab olish mumkin?", "210", "35", "42", "21", "B"),
    (10, "Ko'rsatkichli tengsizlikni yeching: (1/3)^(x² - 1) ≥ 9", "[-1; 1]", "Yechimga ega emas (bo'sh to'plam)", "(-∞; -1] ∪ [1; +∞)", "(-1; 1)", "B"),
    (11, "cos(2x) - 3·cos(x) + 2 = 0 tenglamaning [0; 2π] kesmadagi ildizlari sonini toping.", "2 ta", "3 ta", "4 ta", "5 ta", "C"),
    (12, "To'g'ri prizmaning asosi tomonlari 5 sm, 12 sm va 13 sm bo'lgan uchburchakdan iborat. Prizmaning balandligi 10 sm bo'lsa, uning yon sirti yuzini toping.", "300 sm²", "600 sm²", "360 sm²", "150 sm²", "A"),
    (13, "Hisoblang: log₃2 · log₄3 · log₅4 · log₆5 · log₇6 · log₈7", "1/3", "1/2", "1", "2", "A"),
    (14, "Tengsizlikni yeching: log₃(x - 2) < 1", "(2; 5)", "(-∞; 5)", "(2; 3)", "[2; 5]", "A"),
    (15, "Arifmetik progressiyada S(n) = 2n² + 3n bo'lsa, progressiyaning ayirmasi d ni toping.", "2", "4", "3", "5", "B"),
    (16, "Radiusi 5 sm bo'lgan sharga balandligi 8 sm bo'lgan konus ichki chizilgan. Konus asosining radiusini toping.", "3 sm", "4 sm", "4.5 sm", "5 sm", "B"),
    (17, "Agar f(x) = 3^x + x bo'lsa, f(x) = 10 tenglamaning haqiqiy ildizlari sonini toping.", "2 ta", "1 ta", "0 ta", "3 ta", "B"),
    (18, "y = |x² - 4| funksiya grafigi va y = 3 to'g'ri chizig'i nechta nuqtada kesishadi?", "2 ta", "3 ta", "4 ta", "5 ta", "C"),
    (19, "a(1; 2; -2) va b(2; 0; 1) fazoviy vektorlar orasidagi burchakning kosinusini (cos φ) toping.", "0", "2/3", "4/15", "-4/9", "A"),
    (20, "100! + 1 soni quyidagilardan qaysi biriga qoldiqsiz bo'linadi?", "2 ga", "51 ga", "101 ga", "7 ga", "C"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=10, title=TITLE, start_datetime__date=START.date()).exists():
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
        ('tests_app', '0048_seed_grade11_math_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
