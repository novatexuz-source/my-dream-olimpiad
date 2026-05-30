from django.db import migrations

TEST_TITLE = "6-sinf Matematika: Yuqori Darajali Mantiqiy Test"

DATA = [
    (1, "Hisoblang: -15 - (-24) + (-8) = ?", "-1", "1", "17", "B"),
    (2, "Proporsiyaning noma'lum hadini toping: X/1.2 = 5/3", "2", "1.8", "2.4", "A"),
    (3, "Ikki sonning EKUKi (Eng kichik umumiy karralisi) 60 ga, EKUBi (Eng katta umumiy bo'luvchisi) esa 6 ga teng. Agar sonlardan biri 12 bo'lsa, ikkinchi sonni toping.", "24", "30", "18", "B"),
    (4, "To'g'ri to'rtburchakning bo'yi 20% ga orttirildi, eni esa 20% ga kamaytirildi. Uning yuzi qanday o'zgardi?", "O'zgarmadi", "4% ga kamaydi", "4% ga ortdi", "B"),
    (5, "Jamila shokoladning avval yarmini, keyin qolganining yarmini va yana qolganining yarmini yedi. Shunda shokoladning qancha qismi qoldi?", "1/6 qismi", "1/8 qismi", "1/4 qismi", "B"),
    (6, "Tenglamani yeching: 3 x (2X - 5) - 4X = -23", "-4", "4", "-3", "A"),
    (7, "Xaritada ikki shahar o'rtasidagi masofa 5 sm ga teng. Agar xarita miqyosi (masshtabi) 1 : 200 000 bo'lsa, haqiqiy hayotda bu shaharlar o'rtasidagi masofa necha kilometr?", "10 km", "100 km", "20 km", "A"),
    (8, "Qutida 4 ta qizil, 5 ta yashil va 6 ta ko'k shar bor. Qutiga qaramasdan, ichidan kamida bitta ko'k shar chiqishiga mutlaqo amin bo'lish uchun eng kamida nechta shar olish kerak?", "7 ta", "10 ta", "11 ta", "B"),
    (9, "-5 va 6 sonlari orasida nechta butun son bor? (Ushbu sonlarning o'zi kirmaydi)", "10 ta", "11 ta", "12 ta", "A"),
    (10, "Do'kondagi mahsulot narxi ketma-ket ikki marta 20% dan qimmatlashdi. Mahsulot dastlabki narxiga nisbatan necha foizga qimmatlashgan?", "40% ga", "44% ga", "42% ga", "B"),
    (11, "Quyidagi sonlardan qaysi biri ham 2 ga, ham 3 ga, ham 5 ga qoldiqsiz bo'linadi?", "1250", "3420", "5115", "B"),
    (12, "Velosipedchi tog'ga 10 km/soat tezlik bilan chiqdi va o'sha yo'ldan 15 km/soat tezlik bilan pastga tushdi. Velosipedchining butun yo'l davomidagi o'rtacha tezligini toping.", "12.5 km/soat", "12 km/soat", "11.5 km/soat", "B"),
    (13, "Kasrning maxraji suratidan 5 taga katta. Agar uning suratiga 3, maxrajiga 2 qo'shilsa, kasrning qiymati 3/5 ga teng bo'ladi. Dastlabki kasrni toping.", "4/9", "5/10", "3/8", "C"),
    (14, "A va B qarama-qarshi ishorali sonlar. |A| = 7 va |B| = 4. A - B ayirmaning bo'lishi mumkin bo'lgan eng kichik qiymati nechaga teng?", "-3", "-11", "3", "B"),
    (15, "Idishning 3/7 qismi suv bilan to'la. Agar unga yana 12 litr suv quyilsa, idish butunlay to'ladi. Idish jami necha litr suv sig'diradi?", "21 litr", "28 litr", "35 litr", "A"),
    (16, "Modul ichidagi ifodani hisoblang: |4 - 9| - |12 - 5| = ?", "2", "-2", "12", "B"),
    (17, "Sinfda 30 ta o'quvchi bor. Ulardan 18 tasi matematika to'garagiga, 14 tasi ingliz tili to'garagiga qatnashadi. 5 ta o'quvchi esa hech qaysi to'garakka bormaydi. Nechta o'quvchi ikkala to'garakka ham qatnashadi?", "7 ta", "4 ta", "2 ta", "A"),
    (18, "Uchta sonning o'rtacha arifmetigi 24 ga teng. Agar ularga 40 soni qo'shilsa, to'rtta sonning yangi o'rtacha arifmetigi nechaga teng bo'ladi?", "32", "28", "26", "B"),
    (19, "Bir ishni Alisher 6 soatda, Sardor esa 12 soatda tugatadi. Agar ular birgalikda ishlashsa, shu ishni necha soatda tugatishadi?", "4 soatda", "3 soatda", "5 soatda", "A"),
    (20, "Davriy kasrni oddiy kasrga aylantiring: 0.(6) = ?", "6/10", "2/3", "3/5", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    test, _ = Test.objects.get_or_create(
        subject=subject, grade=6, title=TEST_TITLE,
        defaults={'duration_minutes': 40, 'passing_percentage': 70.0, 'is_active': True},
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
    Test.objects.filter(title=TEST_TITLE, grade=6).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0008_seed_grade5_math'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
