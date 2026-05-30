from django.db import migrations

TEST_TITLE = "9-sinf: Geometriya va Matematika Aralash Test II"

DATA = [
    (1, "To'g'ri burchakli uchburchakning o'tkir burchaklari bissektrisalari kesishishidan hosil bo'lgan o'tmas burchakni toping.", "120°", "135°", "150°", "B"),
    (2, "Agar tanα = 3 bo'lsa, (2sinα - cosα)/(sinα + 3cosα) kasrning qiymatini hisoblang.", "5/6", "1/2", "3/4", "A"),
    (3, "Aylanadan tashqaridagi nuqtadan aylanaga ikkita urinma o'tkazilgan. Urinmalar orasidagi burchak 60° ga, urinish nuqtalari orasidagi masofa (vatar) esa 6√3 sm ga teng. Berilgan nuqtadan aylana markazigacha bo'lgan masofani toping.", "12 sm", "6 sm", "8√3 sm", "A"),
    (4, "Uchburchakning tomonlari x^2 - 3x - 4 = 0 va x^2 - 7x + 12 = 0 tenglamalarning musbat ildizlariga teng. Agar bu uchburchak to'g'ri burchakli bo'lsa, uning yuzini toping.", "6", "12", "5", "A"),
    (5, "Markazi O(2; -1) nuqtada bo'lgan aylana A(5; 3) nuqtadan o'tadi. Shu aylananing uzunligini toping (π soni o'zgarmas qoladi).", "10π", "5π", "25π", "A"),
    (6, "Ikkita o'xshash ko'pburchakning perimetrlari nisbati 2 : 3 kabi. Agar ularning yuzlari yig'indisi 130 sm² bo'lsa, katta ko'pburchakning yuzini toping.", "90 sm²", "40 sm²", "75 sm²", "A"),
    (7, "Koordinatalar tekisligida A(-1; 2), B(3; 5) va C(x; y) nuqtalar berilgan. Agar AB vektor = BC vektor bo'lsa, C nuqtaning koordinatalarini toping.", "(7; 8)", "(5; 7)", "(6; 8)", "A"),
    (8, "Rombning yuzi 24 sm², diagonallaridan biri esa 6 sm. Rombning o'tkir burchagi sinusini (sinα) toping.", "0.8", "0.96", "0.6", "B"),
    (9, "Uchburchakning tomonlari 13 sm, 14 sm va 15 sm. Shu uchburchakka ichki chizilgan aylananing radiusini (r) toping.", "4 sm", "5 sm", "3 sm", "A"),
    (10, "a(2; -3) va b(x; 4) vektorlar o'zaro kollinear (parallel) bo'lsa, x ning qiymatini toping.", "-8/3", "8/3", "-6", "A"),
    (11, "Muntazam oltiburchak ichiga chizilgan aylananing yuzi 27π sm². Shu oltiburchakning perimetrini toping.", "36 sm", "24√3 sm", "24 sm", "A"),
    (12, "Agar sinα · cosα = 0.4 bo'lsa, sin⁴α + cos⁴α ifodaning qiymatini hisoblang.", "0.68", "0.84", "0.32", "A"),
    (13, "Aylananing diametriga perpendikulyar bo'lgan vatar diametrni 2 sm va 8 sm li bo'laklarga ajratadi. Shu vatarning umumiy uzunligini toping.", "8 sm", "4 sm", "10 sm", "A"),
    (14, "Teng yonli trapetsiyaning asoslari 10 sm va 24 sm, yon tomoni esa 25 sm. Trapetsiyaning diagonali uzunligini toping.", "26 sm", "25 sm", "√865 sm", "C"),
    (15, "Radiusi 12 sm bo'lgan doiraning 120° li yoyiga mos keluvchi segmentining yuzini toping (π ≈ 3).", "144 - 36√3", "48 - 12√3", "48 - 24√3", "A"),
    (16, "Uchburchakning burchaklari 1 : 2 : 3 nisbatda. Eng kichik tomoni 5 sm bo'lsa, uning eng katta tomonini toping.", "10 sm", "5√3 sm", "15 sm", "A"),
    (17, "Agar a va b vektorlar uchun |a|=3, |b|=4 va ular orasidagi burchak 60° bo'lsa, |a + b| vektorning uzunligini toping.", "√37", "5", "√13", "A"),
    (18, "To'g'ri burchakli uchburchakning katetlari gipotenuzadagi proeksiyalari 3 va 12 ga teng. Uchburchakning kichik katetini toping.", "3√5", "6", "6√5", "A"),
    (19, "To'g'ri to'rtburchak shaklidagi tomorqaning bo'yi a metr, eni b metr. Agar uning diagonali 25 metr bo'lib, perimetri 70 metr bo'lsa, tomorqaning yuzini toping.", "300 m²", "400 m²", "350 m²", "A"),
    (20, "Muntazam ko'pburchakning diagonallari soni uning tomonlari sonidan 3 marta katta. Bu ko'pburchakning bitta ichki burchagi necha gradusga teng?", "135°", "140°", "120°", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    test, _ = Test.objects.get_or_create(
        subject=subject, grade=9, title=TEST_TITLE,
        defaults={'duration_minutes': 50, 'passing_percentage': 70.0, 'is_active': True},
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
    Test.objects.filter(title=TEST_TITLE, grade=9).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0011_seed_grade9_math'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
