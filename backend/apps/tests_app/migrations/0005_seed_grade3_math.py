from django.db import migrations

TEST_TITLE = "3-sinf Matematika: Murakkablashtirilgan Mantiqiy Test"

DATA = [
    (1, "Uch xonali eng kichik juft son bilan ikki xonali eng katta toq sonning ayirmasini toping.", "1", "3", "0", "A"),
    (2, "Agar bo'linuvchi 56 ga, bo'linma 7 ga teng bo'lsa, bo'luvchining 3 barobar orttirilgan qiymati nechaga teng bo'ladi?", "8", "24", "16", "B"),
    (3, "Ketma-ketlikni mantiqiy davom ettiring: 4, 9, 14, 19, ... Shu ketma-ketlikdagi 6-sonni toping.", "24", "29", "34", "B"),
    (4, "Sinfdagi 15 ta o'quvchi nemis tilini, 12 tasi esa ingliz tilini o'rganadi. Agar 5 ta o'quvchi ikkala tilni ham o'rgansa, sinfda jami nechta o'quvchi bor?", "27 ta", "22 ta", "32 ta", "B"),
    (5, "Sayyoh 24 km yo'lning 1/3 qismini piyoda bosib o'tdi. U yana necha kilometr yo'l yurishi kerak?", "8 km", "16 km", "12 km", "B"),
    (6, "Qoldiqli bo'lishni bajaring: 45 : 6 = ?", "7 (3 qoldiq)", "7 (2 qoldiq)", "6 (9 qoldiq)", "A"),
    (7, "Kvadratning perimetri 36 sm ga teng. Shu kvadratning bir tomonining uzunligini toping.", "6 sm", "9 sm", "12 sm", "B"),
    (8, "Kitob 120 betdan iborat. Sardor birinchi kuni kitobning yarmini, ikkinchi kuni esa qolgan betlarning yarmini o'qidi. Kitobning o'qilmagan nechta beti qoldi?", "30 bet", "60 bet", "45 bet", "A"),
    (9, "Do'konda 5 ta daftar va 3 ta qalam uchun jami 45 tanga to'landi. Agar bitta qalam 5 tanga tursa, bitta daftar necha tanga turadi?", "5 tanga", "6 tanga", "8 tanga", "B"),
    (10, "Agar soat mili kunduzgi 15:00 ni ko'rsatayotgan bo'lsa, bundan 18 soat oldin soat necha bo'lgan?", "Kechasi 21:00", "Ertalabki 09:00", "Kechasi 03:00", "A"),
    (11, "Qaysi amal to'g'ri bajarilgan?", "320 + 180 = 500", "750 - 260 = 510", "450 + 150 = 500", "A"),
    (12, "Onasi 36 yoshda, qizi esa 9 yoshda. Necha yildan keyin onasi qizidan 3 barobar katta bo'ladi?", "3 yildan keyin", "4 yildan keyin", "5 yildan keyin", "B"),
    (13, "Bir xonada 3 ta mushuk bor. Har bir mushukning qarshisida 2 tadan mushuk o'tiribdi. Xonada jami nechta mushuk bor?", "6 ta", "3 ta", "9 ta", "B"),
    (14, "Tenglamani yeching: (X - 15) x 4 = 100", "40", "25", "35", "A"),
    (15, "To'g'ri to'rtburchak shaklidagi bog'ning bo'yi 12 metr, eni esa bo'yining yarmiga teng. Bog'ning yuzini (S) toping.", "36 kv.m", "72 kv.m", "24 kv.m", "B"),
    (16, "Idishda 3 litr suv bor edi. Undan har biri 250 grammdan bo'lgan 4 ta stakanga suv quyib olindi. Idishda qancha suv qoldi?", "1 litr", "2 litr", "1 litr 500 gramm", "B"),
    (17, "Ota va o'g'ilning yoshlari yig'indisi 40 ga teng. 5 yildan keyin ularning yoshlari yig'indisi nechaga teng bo'ladi?", "45", "50", "42", "B"),
    (18, "A x B = 24 va B x C = 12. Agar B = 4 bo'lsa, A + C nechaga teng?", "9", "8", "10", "A"),
    (19, "Fermada tovuqlar va quyonlar bor. Ularning jami boshlari soni 10 ta, oyoqlari soni esa 28 ta. Fermada nechta quyon bor?", "4 ta", "6 ta", "5 ta", "A"),
    (20, "Shunday sonni topingki, uni 8 ga bo'lib, chiqqan javobga 15 ni qo'shsak, eng kichik uch xonali son hosil bo'lsin.", "640", "680", "720", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    test, _ = Test.objects.get_or_create(
        subject=subject,
        grade=3,
        title=TEST_TITLE,
        defaults={'duration_minutes': 30, 'passing_percentage': 70.0, 'is_active': True},
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
    Test.objects.filter(title=TEST_TITLE, grade=3).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0004_seed_grade2_math'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
