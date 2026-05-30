from django.db import migrations

TEST_TITLE = "2-sinf Matematika: Mantiqiy va Murakkab Test"

DATA = [
    (1, "Ikki xonali eng katta son bilan ikki xonali eng kichik sonning ayirmasini toping.", "89", "90", "99", "A"),
    (2, "Ketma-ketlik qanday qoida asosida tuzilgan: 3, 6, 12, 24, ... Bo'sh joyga qaysi son qo'yilishi kerak?", "36", "48", "30", "B"),
    (3, "Jamila xolaning 3 ta o'g'li bor. Har bir o'g'lining bittadan singlisi bor. Jamila xolaning nechta farzandi bor?", "6 ta", "4 ta", "5 ta", "B"),
    (4, "Shifokor bemorga 3 ta tabletka berdi va ularni har yarim soatda (30 minutda) bittadan ichishni aytdi. Bemor hamma tabletkalarni ichib bo'lishi uchun qancha vaqt ketadi?", "1 soat", "1 soat-u 30 minut", "2 soat", "A"),
    (5, "3 ta konfet 6 sent turadi. 5 ta shunday konfet necha sent turadi?", "10 sent", "8 sent", "12 sent", "A"),
    (6, "Amallarni bajaring: 45 - (18 + 12) + 25 = ?", "30", "40", "50", "B"),
    (7, "Noma'lum sonni toping: X + 27 = 63", "36", "46", "44", "A"),
    (8, "Bir tup daraxtga 12 ta chumchuq qo'ngan edi. Ularning 4 tasidan tashqari hammasi uchib ketdi. Daraxtda nechta chumchuq qoldi?", "8 ta", "0 ta", "4 ta", "C"),
    (9, "Yog'ochni 4 bo'lakka ajratish uchun uni necha joyidan kesish kerak?", "4 marta", "3 marta", "5 marta", "B"),
    (10, "To'g'ri to'rtburchakning bo'yi 8 sm, eni esa bo'yidan 3 sm qisqa. Shu to'g'ri to'rtburchakning perimetrini (hamma tomonlari yig'indisini) toping.", "13 sm", "26 sm", "22 sm", "B"),
    (11, "Qaysi ifodaning qiymati eng katta?", "5 x 3", "20 : 2", "4 x 4", "C"),
    (12, "Bo'linuvchi 24 ga, bo'luvchi 3 ga teng. Bo'linmani toping.", "8", "7", "9", "A"),
    (13, "Idishdagi suvning yarmi to'kilgach, idishning og'irligi 5 kg bo'lib qoldi. Agar to'la idishning og'irligi 9 kg bo'lsa, bo'sh idishning o'zi necha kg keladi?", "1 kg", "2 kg", "4 kg", "A"),
    (14, "Simni o'rtasidan buklab, keyin yana o'rtasidan kesishdi. Jami nechta bo'lak sim hosil bo'ldi?", "3 ta", "4 ta", "2 ta", "A"),
    (15, "Velosiped va motosikl poygasida jami 8 ta g'ildirak yerga tegib turibdi. Agar poygada velosipedlar ham, motosikllar ham 2 g'ildirakli bo'lsa, jami nechta transport vositasi qatnashmoqda?", "4 ta", "3 ta", "6 ta", "A"),
    (16, "Bir soatning 1/2 qismi (yarmi) necha minutga teng?", "20 minut", "30 minut", "15 minut", "B"),
    (17, "Otabek 10 yoshda. Ukasi Sardor undan 4 yosh kichik. Sardor tug'ilganda Otabek necha yoshda bo'lgan?", "6 yoshda", "4 yoshda", "5 yoshda", "B"),
    (18, "Hisoblang: 7 x 2 + 18 : 3 = ?", "20", "16", "22", "A"),
    (19, "Shunday sonni topingki, uni 2 barobar oshirib, keyin 5 ni ayirsak, 11 hosil bo'lsin.", "7", "8", "9", "B"),
    (20, "Kvadrat shaklidagi hovlining atrofini panjara bilan o'rashdi. Har bir tomonda 3 tadan ustun ishlatilgan bo'lsa, jami nechta ustun o'rnatilgan? (Burchaklardagi ustunlar umumiy)", "12 ta", "8 ta", "10 ta", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    test, _ = Test.objects.get_or_create(
        subject=subject,
        grade=2,
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
    Test.objects.filter(title=TEST_TITLE, grade=2).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0003_seed_grade1_math'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
