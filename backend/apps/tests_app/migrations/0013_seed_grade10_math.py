from django.db import migrations

TEST_TITLE = "10-sinf: Geometriya va Matematika Aralash Test"

DATA = [
    (1, "Fazoda A(1; -2; 3) va B(3; 2; 1) nuqtalar berilgan. AB kesma o'rtasining koordinata boshigacha (O(0;0;0)) bo'lgan masofasini toping.", "3", "2√2", "√14", "B"),
    (2, "Kubning diagonal kesimi yuzi 16√2 sm² ga teng. Shu kubning hajmini (V) toping.", "64 sm³", "16 sm³", "32 sm³", "A"),
    (3, "Tekislikka o'tkazilgan og'ma tekislik bilan 30° li burchak hosil qiladi. Agar og'maning tekislikdagi proeksiyasi 6√3 sm bo'lsa, berilgan nuqtadan tekislikkacha bo'lgan masofani toping.", "6 sm", "12 sm", "3√3 sm", "A"),
    (4, "To'g'ri prizmaning asosi tomonlari 5 sm, 12 sm va 13 sm bo'lgan uchburchakdan iborat. Prizmaning to'liq sirti yuzi 360 sm² bo'lsa, uning balandligini (h) toping.", "10 sm", "8 sm", "12 sm", "A"),
    (5, "a(2; -1; 3) va b(x; 4; -2) vektorlar o'zaro perpendikulyar bo'lsa, x ning qiymatini toping.", "5", "4", "3", "A"),
    (6, "Fazoda berilgan to'g'ri chiziq va tekislik o'rtasidagi burchak sinusining qiymati sinα = 0.6 ga teng. Og'maning uzunligi 15 sm bo'lsa, uning tekislikdagi proeksiyasini toping.", "12 sm", "9 sm", "10 sm", "A"),
    (7, "Muntazam to'rtburchakli piramidaning asosi yuzi 36, balandligi esa 4 ga teng. Piramidaning apofemasini (yon yog'ining balandligini) toping.", "5", "√13", "6", "A"),
    (8, "Ikki parallel tekislik orasidagi masofa 8 sm. Uzunligi 10 sm bo'lgan kesmaning uchlari shu tekisliklarda yotadi. Kesmaning tekisliklar bilan hosil qilgan burchagi kosinusini (cosα) toping.", "0.6", "0.8", "0.5", "A"),
    (9, "Tetraedrning (uchburchakli piramidaning) barcha qirralari 2√2 sm ga teng. Uning to'liq sirti yuzini toping.", "8√3 sm²", "4√3 sm²", "16 sm²", "A"),
    (10, "To'g'ri parallelepipedning asosi tomonlari 3 sm va 4 sm bo'lgan to'g'ri to'rtburchakdan iborat. Parallelepipedning diagonali asosi tekisligi bilan 60° li burchak hosil qilsa, uning balandligini toping.", "5√3 sm", "5 sm", "5√3/3 sm", "A"),
    (11, "a(1; 2; -2) vektor bilan yo'nalishdosh bo'lgan va uzunligi 9 ga teng bo'lgan vektor koordinatalarini ko'rsating.", "(3; 6; -6)", "(2; 4; -4)", "(3; 3; -3)", "A"),
    (12, "Uch perpendikulyar haqidagi teoremaga ko'ra, tekislikdagi to'g'ri chiziq og'maning proeksiyasiga perpendikulyar bo'lsa, u og'maning o'ziga nisbatan qanday vaziyatda bo'ladi?", "Parallel bo'ladi", "Perpendikulyar bo'ladi", "45° burchak ostida kesishadi", "B"),
    (13, "Muntazam uchburchakli prizmaning barcha qirralari o'zaro teng. Agar uning yon sirti yuzi 48 sm² bo'lsa, asosi tomonining uzunligini toping.", "4 sm", "2 sm", "3 sm", "A"),
    (14, "Fazodagi uchta nuqta koordinatalari: A(2; 1; 0), B(4; 2; 2) va C(6; 3; 4). Bu nuqtalar haqida qaysi fikr to'g'ri?", "Ular bitta to'g'ri chiziqda yotadi", "Ular uchburchak hosil qiladi", "Ular koordinata o'qlarida yotadi", "A"),
    (15, "Ikki yoqli burchak ichidagi nuqtadan uning yoqlariga perpendikulyarlar o'tkazilgan. Agar perpendikulyarlar orasidagi burchak 120° bo'lsa, ikki yoqli burchakning chiziqli burchagini toping.", "60°", "120°", "90°", "A"),
    (16, "Kubning hajmi x² - 16x + 64 = 0 tenglamaning ildiziga teng bo'lsa, shu kubning bitta qirrasi uzunligini toping.", "2 sm", "3 sm", "4 sm", "A"),
    (17, "To'g'ri prizmaning asosi rombdan iborat bo'lib, uning diagonallari 6 sm va 8 sm. Prizmaning balandligi 5 sm bo'lsa, uning yon sirti yuzini toping.", "100 sm²", "120 sm²", "80 sm²", "A"),
    (18, "a(1; 0; 1) va b(0; 1; 1) vektorlar orasidagi burchakni toping.", "60°", "45°", "30°", "A"),
    (19, "Tekislikni kesib o'tuvchi kesmaning uchlari tekislikdan 3 sm va 5 sm masofada joylashgan. Kesma o'rtasidan tekislikkacha bo'lgan masofani toping.", "1 sm", "4 sm", "2 sm", "A"),
    (20, "Muntazam oltiburchakli piramidaning asosi tomoni 2 sm, yon qirrasi esa 4 sm. Piramidaning balandligini (h) toping.", "2√3 sm", "3√2 sm", "3 sm", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    test, _ = Test.objects.get_or_create(
        subject=subject, grade=10, title=TEST_TITLE,
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
    Test.objects.filter(title=TEST_TITLE, grade=10).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0012_seed_grade9_math_2'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
