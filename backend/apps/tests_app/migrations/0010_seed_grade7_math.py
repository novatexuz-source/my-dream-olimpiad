from django.db import migrations

TEST_TITLE = "7-sinf Algebra va Geometriya: Yuqori Darajali Test"

DATA = [
    (1, "Soddalashtiring: (x - 3)^2 - (x + 3)(x - 3) = ?", "-6x + 18", "-6x", "18", "A"),
    (2, "Tenglamalar sistemasini yeching va x·y ko'paytmaning qiymatini toping: 2x + y = 11; 3x - y = 9", "12", "15", "8", "A"),
    (3, "Agar a + b = 7 va a·b = 10 bo'lsa, a^2 + b^2 ning qiymatini hisoblang.", "29", "39", "49", "A"),
    (4, "Ko'paytuvchilarga ajrating: x^3 - 4x = ?", "x(x - 2)^2", "x(x - 2)(x + 2)", "x^2(x - 4)", "B"),
    (5, "Hisoblang: (4^11 · 9^9) / 6^20 = ?", "4/9", "9/4", "1", "A"),
    (6, "y = -3x + 5 funksiya grafigi koordinata o'qlarining qaysi choraklaridan o'tadi?", "I, II, III", "I, II, IV", "II, III, IV", "B"),
    (7, "Agar f(x) = 2x^2 - 3x + 1 bo'lsa, f(-2) ni hisoblang.", "3", "15", "11", "B"),
    (8, "Uchta ketma-ket kelgan toq natural sonlarning yig'indisi 57 ga teng. Shu sonlardan eng kichigini toping.", "17", "19", "15", "A"),
    (9, "Soddalashtiring: (-2a^3b^2)^3 · (3ab^4)^2 = ?", "-72a^11b^14", "-18a^5b^8", "72a^11b^14", "A"),
    (10, "Necha foizli 4 litr tuzli eritmaga 1 litr toza suv qo'shilsa, 16 foizli eritma hosil bo'ladi?", "20%", "25%", "18%", "A"),
    (11, "3^2026 soni qaysi raqam bilan tugaydi?", "3", "9", "1", "B"),
    (12, "Tenglamani yeching: |2x - 5| = 7", "6 va -1", "6", "1 va -6", "A"),
    (13, "Grafiklar kesishish nuqtasini toping: y = 2x - 3 va y = -x + 6", "(3; 3)", "(2; 1)", "(3; 0)", "A"),
    (14, "Uchburchakning ikkita ichki burchagi 45° va 65° ga teng. Shu uchburchakning eng katta tashqi burchagini toping.", "135°", "110°", "115°", "A"),
    (15, "To'g'ri burchakli uchburchakning o'tkir burchaklaridan biri 30° ga, gipotenuzasi esa 12 sm ga teng. Shu burchak qarshisidagi katetning uzunligini toping.", "6 sm", "8 sm", "4 sm", "A"),
    (16, "Qo'shni burchaklardan biri ikkinchisidan 4 barobar katta. Shu burchaklardan kichigini toping.", "36°", "45°", "30°", "A"),
    (17, "Uchburchakning tomonlari a, b va c bo'lsa, quyidagi munosabatlardan qaysi biri har doim o'rinli (Uchburchak tengsizligi)?", "a + b <= c", "a + b > c", "a - b > c", "B"),
    (18, "Ikki parallel to'g'ri chiziqni uchinchi to'g'ri chiziq kesib o'tganda hosil bo'lgan ichki bir tomonli burchaklardan biri 70° bo'lsa, ikkinchisini toping.", "70°", "110°", "20°", "B"),
    (19, "Teng yonli uchburchakning perimetri 26 sm, asosi esa 6 sm. Uning yon tomoni uzunligini toping.", "10 sm", "13 sm", "8 sm", "A"),
    (20, "Uchburchakning barcha tashqi burchaklari yig'indisi nechaga teng?", "180°", "360°", "540°", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    test, _ = Test.objects.get_or_create(
        subject=subject, grade=7, title=TEST_TITLE,
        defaults={'duration_minutes': 45, 'passing_percentage': 70.0, 'is_active': True},
    )

    if test.questions.exists():
        return

    for order, text, a, b, c, correct in DATA:
        Question.objects.create(
            test=test, order_number=order, question_text=text,
            option_a=a, option_b=b, option_c=c, option_d="", correct_answer=correct,
        )


def unseed(apps, schema_editor):
    Test = apps.get_model('tests_app', 'Test')
    Test.objects.filter(title=TEST_TITLE, grade=7).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0009_seed_grade6_math'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
