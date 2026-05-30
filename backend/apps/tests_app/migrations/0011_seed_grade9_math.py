from django.db import migrations

TEST_TITLE = "9-sinf: Geometriya va Matematika Aralash Test"

DATA = [
    (1, "To'g'ri burchakli uchburchakning katetlari yig'indisi 17 sm, gipotenuzasi esa 13 sm. Shu uchburchakning yuzini toping.", "30 sm²", "60 sm²", "40 sm²", "A"),
    (2, "Koordinatalar sistemasida a(x; 3) va b(3; -2) vektorlar berilgan. x ning qanday qiymatida bu vektorlarning uzunliklari (modullari) teng bo'ladi?", "±1", "±2", "±√3", "B"),
    (3, "Uchburchakning ikki tomoni 3 sm va 5 sm ga teng. Uchinchi tomonining bo'lishi mumkin bo'lgan eng katta va eng kichik butun qiymatlari ko'paytmasini toping.", "21", "15", "24", "A"),
    (4, "Radiusi 10 sm bo'lgan aylanaga tashqi chizilgan muntazam ko'pburchakning perimetri 60 sm. Shu ko'pburchakning yuzini toping.", "600 sm²", "300 sm²", "150 sm²", "B"),
    (5, "Agar sinα + cosα = 1.2 bo'lsa, sinα · cosα ko'paytmaning qiymatini toping.", "0.22", "0.44", "0.2", "A"),
    (6, "To'g'ri to'rtburchakning bo'yi enidan 3 sm uzun. Agar uning yuzi 40 sm² bo'lsa, to'g'ri to'rtburchakning perimetrini toping.", "26 sm", "13 sm", "28 sm", "A"),
    (7, "Tekislikda 5 ta nuqta berilgan bo'lib, ularning hech qaysi uchtasi bir to'g'ri chiziqda yotmaydi. Bu nuqtalarni juft-juft qilib tutashtirish orqali nechta har xil kesma hosil qilish mumkin?", "15 ta", "10 ta", "20 ta", "B"),
    (8, "Teng yonli uchburchakning asosi yon tomonidan 2 sm qisqa. Perimetri 16 sm bo'lsa, uchburchakning asosi necha sm?", "6 sm", "4 sm", "5 sm", "B"),
    (9, "Aylananing ikkita vatari kesishish nuqtasidan birinchisi 4 sm va 9 sm li bo'laklarga, ikkinchisi esa x va x+5 sm li bo'laklarga ajraldi. x ning qiymatini toping.", "3 sm", "4 sm", "6 sm", "B"),
    (10, "Kvadrat ichiga chizilgan aylananing yuzi 16π sm². Shu kvadratning yuzini toping.", "32 sm²", "64 sm²", "16 sm²", "B"),
    (11, "Uchburchak burchaklari 2 : 3 : 7 nisbatda. Shu uchburchakning eng katta tashqi burchagini toping.", "105°", "150°", "135°", "B"),
    (12, "A(1; 2) va B(4; 6) nuqtalar orasidagi masofani toping.", "5", "7", "√13", "A"),
    (13, "Agar muntazam ko'pburchakning bitta tashqi burchagi 45° bo'lsa, uning nechta diagonali bor?", "20 ta", "8 ta", "14 ta", "A"),
    (14, "Rombning diagonallari 3 : 4 nisbatda, yuzi esa 24 sm². Rombning balandligini toping.", "4.8 sm", "5 sm", "4 sm", "A"),
    (15, "Markazi O(0;0) nuqtada bo'lgan aylana M(-3; 4) nuqtadan o'tadi. Quyidagi nuqtalardan qaysi biri ham shu aylanada yotadi?", "(5; 0)", "(2; 3)", "(-4; -4)", "A"),
    (16, "To'g'ri burchakli uchburchakning katetlaridan biri 8 sm, unga ichki chizilgan aylananing radiusi esa 2 sm. Gipotenuzaning uzunligini toping.", "10 sm", "17 sm", "15 sm", "A"),
    (17, "Trapetsiyaning asoslari 2 : 3 nisbatda, balandligi 6 sm va yuzi 30 sm² ga teng. Trapetsiyaning katta asosini toping.", "4 sm", "6 sm", "8 sm", "B"),
    (18, "Uchburchakning ikki tomoni 6 sm va 10 sm. Ular orasidagi burchak kosinusi cosα = -0.5 ga teng. Uchburchakning uchinchi tomonini toping.", "14 sm", "12 sm", "16 sm", "A"),
    (19, "Uzunligi 12 sm bo'lgan kesma 3:4:5 nisbatda uch bo'lakka ajratildi. Chetki bo'laklarning o'rtalari orasidagi masofani toping.", "8 sm", "9 sm", "7.5 sm", "A"),
    (20, "Teng yonli trapetsiyaning diagonallari o'zaro perpendikulyar. Agar trapetsiyaning balandligi 8 sm bo'lsa, uning yuzini toping.", "32 sm²", "64 sm²", "48 sm²", "B"),
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
        ('tests_app', '0010_seed_grade7_math'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
