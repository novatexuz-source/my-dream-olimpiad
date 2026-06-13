# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Matematika 5-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Hisoblang va kasrli ifodaning yakuniy qiymatini toping: (3.2 × 1.25 - 0.6) / (0.5 × 2.4 + 0.5)", "2", "2.5", "1.8", "3", "A"),
    (2, "Amallarni ketma-ket bajarib, qiymatini aniqlang: (2 1/3 + 1 3/4) ÷ 1 1/6 - 1.5", "2 4/13", "2 5/13", "2", "2.5", "C"),
    (3, "To'g'ri burchakli parallelepipedning bo'yi 12 sm, eni bo'yining 75% ini, balandligi esa enining 2/3 qismini tashkil qiladi. Parallelepipedning to'la sirti yuzini toping.", "432 sm²", "468 sm²", "512 sm²", "384 sm²", "B"),
    (4, "Sinfdagi o'g'il bolalar soni qizlar sonidan 25% ga ko'p. Qizlar soni sinfdagi jami o'quvchilar sonining necha foizini tashkil qiladi?", "40%", "44%", "45%", "50%", "B"),
    (5, "Quyidagi ko'paytmaning oxirida nechta nol raqami bor: 1 × 2 × 3 × 4 × ... × 25?", "4 ta", "5 ta", "6 ta", "3 ta", "C"),
    (6, "Tenglamani yeching va X ning qiymatini toping: 1200 ÷ [450 - (15 × X + 30)] = 4", "10", "8", "12", "6", "B"),
    (7, "Kema daryo oqimi bo'ylab 4 soatda 96 km, oqimga qarshi esa 6 soatda 108 km yo'l yurdi. Daryo oqimining tezligini (km/h) toping.", "3 km/h", "2 km/h", "4 km/h", "2.5 km/h", "A"),
    (8, "Idishga ma'lum miqdorda suv quyildi. Agar idishdagi suvga yana amaldagi suvning 40% i miqdorida suv qo'shilsa, idishning yarmi (50% i) to'ladi. Agar dastlabki suvdan 5 litr to'kib tashlansa, idishning 1/4 qismi to'la qoladi. Idish jami necha litr suv sig'dira oladi?", "60 litr", "40 litr", "50 litr", "80 litr", "B"),
    (9, "Eng kichik to'rt xonali natural son bilan eng katta uch xonali natural sonning ayirmasiga tub sonlar qatorining dastlabki uchta hadining ko'paytmasini qo'shing. Natija nechaga teng?", "31", "30", "41", "29", "A"),
    (10, "Uchta sonning o'rta arifmetigi 35 ga teng. Agar ularga to'rtinchi son qo'shilsa, ularning o'rta arifmetigi 38 ga teng bo'ladi. Qo'shilgan to'rtinchi sonni toping.", "47", "44", "49", "51", "A"),
    (11, "Proporsiyaning noma'lum hadini toping: (2 1/2) / X = (1 3/4) / 2.1", "3", "2.8", "3.2", "2.5", "A"),
    (12, "Ikki shahar orasidagi masofa xaritada 6 sm ga teng. Agar xaritaning miqyosi (masshtabi) 1:2 500 000 bo'lsa, ikki shahar orasidagi haqiqiy masofa necha km bo'ladi?", "150 km", "120 km", "180 km", "200 km", "A"),
    (13, "A = {X | X ≤ 15, X ∈ N} to'plami berilgan. Bu to'plamning ichidagi faqat tub sonlardan iborat bo'lgan qism to'plamining elementlari soni nechta?", "5 ta", "6 ta", "7 ta", "8 ta", "B"),
    (14, "Sayyoh butun yo'lning 35% ini birinchi kuni, ikkinchi kuni esa qolgan yo'lning 60% ini bosib o'tdi. Agar uchinchi kunga 52 km yo'l qolgan bo'lsa, butun yo'lning uzunligi necha km?", "200 km", "250 km", "180 km", "300 km", "A"),
    (15, "Tomonlari 16 sm va 10 sm bo'lgan to'g'ri to'rtburchak berilgan. Agar uning bo'yi 25% ga oshirilib, eni 20% ga kamaytirilsa, to'rtburchakning yuzi qanday o'zgaradi?", "5% ga kamayadi", "O'zgarmadi", "4% ga ortdi", "2% ga kamaydi", "B"),
    (16, "Hozir ota 42 yoshda, o'g'li esa 12 yoshda. Necha yildan keyin otaning yoshi o'g'lining yoshidan 3 marta katta bo'ladi?", "3 yildan keyin", "4 yildan keyin", "5 yildan keyin", "2 yildan keyin", "A"),
    (17, "7/12 va 5/18 kasrlarning ayirmasini toping va uni davriy o'nli kasr ko'rinishida ifodalang.", "0.30(5)", "0.31(6)", "0.41(6)", "0.20(7)", "A"),
    (18, "Uzunligi 150 m bo'lgan poyezd tekis harakat qilib, yo'l chetidagi simyog'och yonidan 9 sekundda o'tib ketdi. Ushbu poyezd xuddi shu tezlik bilan uzunligi 450 m bo'lgan platformadan jami necha sekundda to'liq o'tib ketadi?", "27 sekund", "36 sekund", "30 sekund", "24 sekund", "B"),
    (19, "|-5.25| ÷ |+0.25| - |-12| × (-0.5) ifodaning qiymatini hisoblang.", "15", "27", "21", "18", "B"),
    (20, "Bir guruh ishchilar ma'lum bir ishni 12 kunda bajarishlari kerak edi. Ish boshlanishidan oldin guruhga yana 4 ta ishchi qo'shildi va shu sababli ish 9 kunda yakunlandi. Dastlab guruhda nechta ishchi bo'lgan?", "12 ta", "8 ta", "10 ta", "16 ta", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=5, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=5,
        title=TITLE,
        duration_minutes=20,
        passing_percentage=0.0,
        is_active=True,
        start_datetime=START,
        end_datetime=END,
    )

    for order, text, a, b, c, d, correct in DATA:
        Question.objects.create(
            test=test,
            order_number=order,
            question_text=text,
            option_a=a,
            option_b=b,
            option_c=c,
            option_d=d,
            correct_answer=correct,
        )


def unseed(apps, schema_editor):
    Test = apps.get_model('tests_app', 'Test')
    Test.objects.filter(title=TITLE, grade=5).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0042_seed_grade4_math_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
