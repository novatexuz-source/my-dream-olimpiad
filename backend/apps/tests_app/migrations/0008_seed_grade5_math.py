from django.db import migrations

TEST_TITLE = "5-sinf Matematika: Mantiqiy va Murakkab Test"

DATA = [
    (1, "Ikki sonning ko'paytmasi 120 ga teng. Agar ko'paytuvchilardan biri 3 barobar orttirilib, ikkinchisi 2 barobar kamaytirilsa, yangi ko'paytma nechaga teng bo'ladi?", "180", "240", "60", "A"),
    (2, "Kasrlarni taqqoslang: A = 7/8 va B = 8/9. Quyidagi munosabatlardan qaysi biri to'g'ri?", "A > B", "A < B", "A = B", "B"),
    (3, "Idishdagi sutning dastlab 1/3 qismi, keyin esa qolgan sutning 1/2 qismi ichildi. Idishda dastlabki sutning qancha qismi qoldi?", "1/3 qismi", "1/2 qismi", "1/6 qismi", "A"),
    (4, "To'g'ri burchakning 3/5 qismi necha gradusga teng bo'ladi?", "54 daraja", "60 daraja", "36 daraja", "A"),
    (5, "Sayyoh birinchi kuni yo'lning 40% ini, ikkinchi kuni esa qolgan 120 km yo'lni bosib o'tdi. Umumiylikda yo'lning uzunligi necha kilometr?", "200 km", "300 km", "240 km", "A"),
    (6, "Amallarni bajaring va o'nli kasr ko'rinishida yozing: 2.5 x 4 - 3.6 : 0.6 = ?", "4", "6.4", "3.4", "A"),
    (7, "To'g'ri burchakli parallelepipedning bo'yi 5 sm, eni 4 sm va balandligi 3 sm. Agar uning barcha qirralari uzunligi 2 barobar orttirilsa, uning hajmi (V) necha barobar ortadi?", "2 barobar", "4 barobar", "8 barobar", "C"),
    (8, "Katerning oqim bo'ylab tezligi 24 km/soat, oqimga qarshi tezligi esa 18 km/soat. Daryo oqimining tezligini toping.", "3 km/soat", "6 km/soat", "2.5 km/soat", "A"),
    (9, "Tenglamani yeching: 3.5 x X - 1.2 = 5.8", "2", "2.5", "1.8", "A"),
    (10, "Do'konda olmaning kilosi 15 000 so'm turadi. Olma narxi dastlab 10% ga arzonlashdi, keyin esa yangi narxi yana 10% ga qimmatlashdi. Olmaning oxirgi narxi necha so'm bo'ldi?", "15 000 so'm", "14 850 so'm", "15 150 so'm", "B"),
    (11, "Ketma-ket kelgan 5 ta toq sonning o'rtacha arifmetigi 15 ga teng. Shu sonlardan eng kichigini toping.", "11", "13", "9", "A"),
    (12, "Sinfdagi o'g'il bolalar soni qizlar sonining 3/4 qismini tashkil qiladi. Agar sinfda jami 28 ta o'quvchi bo'lsa, o'g'il bolalar nechta?", "12 ta", "16 ta", "15 ta", "A"),
    (13, "Teng tomonli uchburchakning perimetri to'g'ri to'rtburchakning perimetriga teng. To'g'ri to'rtburchakning bo'yi 7 sm, eni 5 sm bo'lsa, uchburchakning bir tomoni uzunligi necha sm?", "6 sm", "8 sm", "9 sm", "B"),
    (14, "0, 3, 5, 7 raqamlaridan ularni takrorlamasdan nechta har xil to'rt xonali sonlar tuzish mumkin?", "24 ta", "18 ta", "12 ta", "B"),
    (15, "Hisoblang: (1 - 1/2) x (1 - 1/3) x (1 - 1/4) x (1 - 1/5) = ?", "1/5", "4/5", "1/20", "A"),
    (16, "Agar soatning minut mili 120 darajaga burilsa, qancha vaqt (minut) o'tgan bo'ladi?", "15 minut", "20 minut", "25 minut", "B"),
    (17, "Ota 36 yoshda, o'g'li esa 12 yoshda. Necha yil oldin otaning yoshi o'g'lining yoshidan 4 barobar katta bo'lgan?", "4 yil oldin", "3 yil oldin", "6 yil oldin", "A"),
    (18, "Uzunligi 60 metr bo'lgan poyezd simyog'och yonidan 6 soniyada o'tib ketdi. Poyezdning tezligi soatiga necha kilometr (km/soat)?", "36 km/soat", "10 km/soat", "60 km/soat", "A"),
    (19, "Fermadagi sigirlar uchun 30 kunga yetadigan ozuqa bor edi. 10 kundan keyin fermaga yana xuddi shuncha sigir olib kelindi. Qolgan ozuqa barcha sigirlarga yana necha kunga yetadi?", "10 kunga", "20 kunga", "15 kunga", "A"),
    (20, "Idishga ma'lum miqdorda suv quyildi. Har kuni undagi suv miqdori 2 barobar ko'payadi. Agar idish 10-kuni to'lgan bo'lsa, uning yarmi nechanchi kuni to'lgan edi?", "5-kuni", "9-kuni", "8-kuni", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    test, _ = Test.objects.get_or_create(
        subject=subject, grade=5, title=TEST_TITLE,
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
    Test.objects.filter(title=TEST_TITLE, grade=5).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0007_seed_grade4_math'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
