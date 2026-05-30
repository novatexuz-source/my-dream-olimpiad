from django.db import migrations

TEST_TITLE = "1-sinf Matematika: Mantiqiy va Qiyinlashtirilgan Test"

DATA = [
    (1, "Lola va Aziza jami 6 ta kitob o'qishdi. Ular bir xil miqdorda kitob o'qigan bo'lsa, Lola nechta kitob o'qigan?", "2", "3", "4", "B"),
    (2, "Ketma-ketlikni davom ettiring: 2, 4, 6, 8, ... Keyingi son qaysi?", "9", "10", "12", "B"),
    (3, "Agar kamayuvchi 9 ga teng bo'lib, ayirma 5 bo'lsa, ayriluvchini toping:", "4", "14", "3", "A"),
    (4, "Stolning 4 ta burchagi bor edi. Undan bitta burchagi kesib tashlansa, stolning nechta burchagi qoladi?", "3", "4", "5", "C"),
    (5, "Avtobusda 5 ta yo'lovchi bor edi. Birinchi bekatda 3 ta yo'lovchi tushdi va 4 ta yo'lovchi chiqdi. Avtobusda nechta yo'lovchi bo'ldi?", "6", "5", "7", "A"),
    (6, "Qaysi ifoda to'g'ri?", "10 - 4 > 5", "3 + 4 < 6", "8 - 2 = 5", "A"),
    (7, "Akmal ukasidan 3 yosh katta. 2 yildan keyin Akmal ukasidan necha yosh katta bo'ladi?", "5", "3", "1", "B"),
    (8, "Bir xonali sonlar ichida eng kattasidan eng kichik natural sonni ayirsak necha qoladi?", "8", "9", "0", "A"),
    (9, "Shoxda 5 ta qush o'tirgandi. Ovchi bitta qushni otib tushirdi. Shoxda nechta qush qoldi?", "4", "0 (qolganlari qo'rqib uchib ketdi)", "5", "B"),
    (10, "Doiraning nechta burchagi va tomoni bor?", "1 ta burchagi bor", "Burchagi ham, tomoni ham yo'q", "2 ta tomoni bor", "B"),
    (11, "Sonli jumboq: ? + ? = 10. Agar so'roq belgilari o'rnida bir xil sonlar tursa, so'roq belgisi o'rnida qaysi son bor?", "4", "5", "6", "B"),
    (12, "Ali dushanba kuni 2 sahifa, seshanba kuni esa dushanbadagidan 2 sahifa ko'p kitob o'qidi. Ali ikki kunda jami nechta sahifa o'qigan?", "4", "6", "8", "B"),
    (13, "Agar bugun payshanba bo'lsa, kecha qaysi kun edi?", "Chorshanba", "Juma", "Seshanba", "A"),
    (14, "12 sonida nechta o'nlik va nechta birlik bor?", "2 ta o'nlik, 1 ta birlik", "1 ta o'nlik, 2 ta birlik", "12 ta o'nlik", "B"),
    (15, "Qalam daftardan uzun, daftar esa chizg'ichdan uzun. Eng uzuni qaysi?", "Chizg'ich", "Daftar", "Qalam", "C"),
    (16, "Toshning vazni 2 kilogramm. Unga yana o'zining yarmi qadar og'irlik qo'shilsa, tosh necha kg bo'ladi?", "3 kg", "4 kg", "5 kg", "A"),
    (17, "20 sonidan bitta oldin keladigan sonni toping:", "21", "19", "10", "B"),
    (18, "Likopchada 3 ta nok bor edi. 3 ta qizcha bittadan nokni olishdi, lekin likopchada bitta nok qoldi. Bu qanday sodir bo'ldi?", "Bitta qizcha nokni likopchasi bilan birga olgan", "Noklar ko'payib qolgan", "Qizchalardan biri nokni yemagan", "A"),
    (19, "Hisoblang: 15 - 5 + 3 = ?", "7", "10", "13", "C"),
    (20, "Qaysi yig'indi eng katta qiymatga ega?", "7 + 5", "9 + 4", "8 + 3", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    test, _ = Test.objects.get_or_create(
        subject=subject,
        grade=1,
        title=TEST_TITLE,
        defaults={'duration_minutes': 30, 'passing_percentage': 70.0, 'is_active': True},
    )

    if test.questions.exists():
        return

    for order, text, a, b, c, correct in DATA:
        Question.objects.create(
            test=test,
            order_number=order,
            question_text=text,
            option_a=a,
            option_b=b,
            option_c=c,
            option_d="",
            correct_answer=correct,
        )


def unseed(apps, schema_editor):
    Test = apps.get_model('tests_app', 'Test')
    Test.objects.filter(title=TEST_TITLE, grade=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0002_test_end_datetime_test_start_datetime'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
