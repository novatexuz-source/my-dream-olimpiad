from django.db import migrations

TEST_TITLE = "4-sinf Matematika: Yuqori Darajali Mantiqiy Test"

DATA = [
    (1, "Eng kichik besh xonali son bilan eng katta to'rt xonali sonning ayirmasini toping.", "1", "10", "9", "A"),
    (2, "Ikki shahar o'rtasidagi masofa 240 km. Avtomobil bu masofani 60 km/soat tezlik bilan bosib o'tdi. U orqaga qaytishda tezligini 20 km/soatga oshirdi. Avtomobil orqaga qaytish uchun qancha vaqt sarflagan?", "4 soat", "3 soat", "5 soat", "B"),
    (3, "Tenglamani yeching: 4 x (X + 120) - 150 = 650", "80", "100", "120", "A"),
    (4, "To'g'ri to'rtburchak shaklidagi maydonning yuzi 72 kv.m. Agar uning eni 6 metr bo'lsa, shu maydonning atrofini bir qator sim bilan o'rash uchun necha metr sim kerak bo'ladi?", "36 metr", "18 metr", "32 metr", "A"),
    (5, "Jamila kitobning 3/5 qismini o'qidi. Agar u yana 20 sahifa o'qisa, kitob butunlay tugaydi. Kitob jami necha sahifadan iborat?", "60 sahifa", "50 sahifa", "100 sahifa", "B"),
    (6, "Qoldiqli bo'lishda bo'luvchi 15 ga teng bo'lsa, qoldiq bo'lishi mumkin bo'lgan eng katta son nechaga teng?", "16", "14", "1", "B"),
    (7, "Onasi 32 yoshda, uchta farzandi esa mos ravishda 2, 4 va 6 yoshda. Necha yildan keyin farzandlarining yoshlari yig'indisi onasining yoshiga teng bo'ladi?", "10 yildan keyin", "8 yildan keyin", "6 yildan keyin", "A"),
    (8, "3 ta daftar va 2 ta ruchka uchun jami 22 000 so'm to'landi. 3 ta daftar va 5 ta ruchka uchun esa 37 000 so'm to'landi. Bitta daftarning narxini toping.", "5 000 so'm", "4 000 so'm", "6 000 so'm", "B"),
    (9, "Ketma-ket kelgan uchta natural sonning yig'indisi 45 ga teng. Shu sonlardan eng kattasini toping.", "15", "16", "17", "B"),
    (10, "Poyezd uzunligi 500 metr bo'lgan tunneldan 60 soniyada o'tib ketdi. Poyezdning tezligi 15 m/s bo'lsa, poyezdning o'z uzunligi necha metr?", "400 metr", "300 metr", "200 metr", "A"),
    (11, "Quyidagi sonlardan qaysi biri ham 3 ga, ham 5 ga qoldiqsiz bo'linadi?", "345", "230", "513", "A"),
    (12, "Agar kubning barcha qirralari uzunliklari yig'indisi 48 sm bo'lsa, uning bitta qirrasi uzunligi necha sm?", "8 sm", "4 sm", "6 sm", "B"),
    (13, "Idishning 1/4 qismiga suv quyilganda og'irligi 7 kg chiqdi. To'liq suv bilan to'ldirilganda esa 22 kg chiqdi. Bo'sh idishning og'irligi necha kg?", "2 kg", "3 kg", "5 kg", "A"),
    (14, "Ikki sonning yig'indisi 180 ga teng. Ulardan biri ikkinchisidan 4 barobar katta. Kichik sonni toping.", "36", "45", "30", "A"),
    (15, "Soat mili bir sutkada (24 soatda) necha marta minut mili bilan ustma-ust tushadi?", "24 marta", "22 marta", "12 marta", "B"),
    (16, "Devor soati har soatda 2 daqiqa orqada qoladi. Agar soat ertalabki 08:00 da to'g'rilab qo'yilgan bo'lsa, kechki 20:00 da soat necha bo'lib ko'rinadi?", "19:36", "19:40", "20:24", "A"),
    (17, "O'g'il bola va qiz bola navbatma-navbat tosh terishmoqda. Birinchi bo'lib qiz bola 1 ta tosh oldi, o'g'il bola 2 ta, keyin qiz bola 3 ta, o'g'il bola 4 ta va hokazo. Oxirgi marta qiz bola tosh olganda savatda tosh qolmadi. Jami terilgan toshlar soni qaysi son bo'lishi mumkin?", "15", "20", "25", "A"),
    (18, "Agar A + A + B = 17 va A + B + B = 16 bo'lsa, A x B qiymati nechaga teng?", "30", "20", "24", "A"),
    (19, "Uzunligi 12 sm, eni 8 sm bo'lgan to'g'ri to'rtburchakdan tomoni 4 sm bo'lgan kvadrat kesib olindi. Qolgan shaklning yuzi necha kv.sm bo'ladi?", "80", "96", "48", "A"),
    (20, "Sinfdagi o'quvchilar partalarga 2 tadan o'tirishsa, 3 ta o'quvchi joy yetmay tik turib qoladi. Agar 3 tadan o'tirishsa, 2 ta parta bo'sh qoladi. Sinfda nechta parta bor?", "9 ta", "8 ta", "7 ta", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    test, _ = Test.objects.get_or_create(
        subject=subject, grade=4, title=TEST_TITLE,
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
    Test.objects.filter(title=TEST_TITLE, grade=4).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0006_fix_grade3_q12'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
