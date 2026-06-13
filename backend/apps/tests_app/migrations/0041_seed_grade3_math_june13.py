# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Matematika 3-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Uch xonali sonning raqamlari yig'indisi 24 ga teng. Shu sonning raqamlari ko'paytmasi eng ko'pi bilan nechaga teng bo'lishi mumkin?", "486", "504", "512", "432", "C"),
    (2, "Kvadratning yuzi 81 sm². Bo'yi shu kvadratning perimetriga teng, eni esa kvadratning bitta tomoniga teng bo'lgan to'g'ri to'rtburchakning yuzini toping.", "324 sm²", "243 sm²", "162 sm²", "288 sm²", "A"),
    (3, "Tenglamani yeching: 5 × (X + 240) - 120 = 1480. X ning qiymatini aniqlang.", "80", "90", "100", "60", "A"),
    (4, "Uchta javonda jami 120 ta kitob bor. Birinchi javondan ikkinchisiga 10 ta kitob o'tkazilgandan keyin, uchala javondagi kitoblar soni teng bo'lib qoldi. Dastlab birinchi javonda nechta kitob bo'lgan?", "40 ta", "50 ta", "60 ta", "30 ta", "B"),
    (5, "Ikki shahar orasidagi masofani yuk mashinasi 60 km/h tezlik bilan 4 soatda bosib o'tadi. Yengil mashina shu masofani 3 soatda bosib o'tishi uchun tezligini necha km/h ga oshirishi kerak?", "20 km/h", "80 km/h", "15 km/h", "25 km/h", "A"),
    (6, "Qutida qizil, ko'k va yashil qalamlar bor. Qizildan boshqa qalamlar soni 18 ta, ko'kdan boshqa qalamlar soni 14 ta, yashildan boshqa qalamlar soni 12 ta bo'lsa, qutida jami nechta qalam bor?", "22 ta", "32 ta", "44 ta", "24 ta", "A"),
    (7, "Do'konda 5 kg olma va 4 kg banan uchun jami 58 ming so'm to'landi. 3 kg olma va 4 kg banan esa 46 ming so'm turadi. 1 kg banan necha pul turadi?", "6 ming so'm", "7 ming so'm", "8 ming so'm", "5 ming so'm", "B"),
    (8, "5 ta ketma-ket kelgan juft sonning yig'indisi 120 ga teng. Shu sonlardan eng kattasini toping.", "24", "26", "28", "30", "C"),
    (9, "Kema daryo oqimi bo'ylab 3 soatda 72 km yo'l yurdi. Agar daryo oqimining tezligi 4 km/h bo'lsa, kema oqimga qarshi 4 soatda necha km yo'l yuradi?", "72 km", "64 km", "80 km", "84 km", "B"),
    (10, "12 ta odam davrada uchrashib, bir-birlari bilan bir marta qo'l berib ko'rishishdi. Jami qo'l berib ko'rishishlar soni nechta bo'ladi?", "66 ta", "132 ta", "72 ta", "60 ta", "A"),
    (11, "Ota 40 yoshda, uning 3 ta farzandi esa 6, 8 va 10 yoshda. Necha yildan keyin otaning yoshi farzandlari yoshlarining yig'indisiga teng bo'ladi?", "6 yildan keyin", "8 yildan keyin", "10 yildan keyin", "12 yildan keyin", "B"),
    (12, "Quyidagi ko'paytmaning oxirgi raqamini aniqlang: 1 × 2 × 3 × 4 × 5 × 6 × 7 × 8 × 9", "0", "5", "2", "6", "A"),
    (13, "To'g'ri to'rtburchakning bo'yi 10 sm, eni esa undan 2,5 marta qisqa. Shu to'rtburchak burchaklaridan birining bissektrisasi uni ikkita shaklga ajratadi. Shu shakllardan kattasining yuzini toping.", "32 sm²", "40 sm²", "24 sm²", "36 sm²", "A"),
    (14, "Soat 15:40 bo'lganda, soatning minut va soat millari orasidagi burchak necha gradusga teng bo'ladi?", "120°", "130°", "140°", "150°", "B"),
    (15, "Idishda ma'lum miqdorda sut bor edi. Unga yana o'zichalik sut qo'shildi va undan 15 litr ishlatildi. Keyin qolgan sutga yana o'sha qolgan sutchalik qo'shilganda jami 30 litr sut bo'ldi. Dastlab idishda necha litr sut bo'lgan?", "15 litr", "20 litr", "25 litr", "18 litr", "A"),
    (16, "Uzunligi 100 metr bo'lgan poyezd uzunligi 300 metr bo'lgan ko'prikdan 20 sekundda butunlay o'tib ketdi. Poyezdning tezligi sekundiga necha metr?", "15 m/s", "20 m/s", "25 m/s", "30 m/s", "B"),
    (17, "Fermadagi sigirlar va g'ozlarning jami boshlari soni 30 ta, oyoqlari soni esa 84 ta. Fermada nechta g'oz bor?", "18 ta", "12 ta", "15 ta", "16 ta", "A"),
    (18, "A, B, C va D o'quvchilar olimpiadada dastlabki 4 ta o'rinni egallashdi. Agar A birinchi emas, B esa ikkinchi emasligi ma'lum bo'lsa, ular o'rinlarni necha xil usulda bo'lishib olishlari mumkin?", "14 xil", "12 xil", "16 xil", "18 xil", "A"),
    (19, "Bir xil 6 ta daftar va 4 ta qalam 4400 so'm turadi. 3 ta shunday daftar va 4 ta qalam esa 2600 so'm turadi. 1 ta daftar qancha turadi?", "500 so'm", "600 so'm", "700 so'm", "400 so'm", "B"),
    (20, "Ikkita to'g'ri chiziq kesishganda hosil bo'lgan burchaklardan uchtasining yig'indisi 280° ga teng. Shu burchaklardan eng kichigini toping.", "80°", "100°", "60°", "70°", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=3, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=3,
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
    Test.objects.filter(title=TITLE, grade=3).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0040_seed_grade2_math_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
