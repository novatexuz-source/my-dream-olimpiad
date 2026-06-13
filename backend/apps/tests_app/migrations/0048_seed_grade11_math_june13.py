# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Matematika 11-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "f(x) = x³ - 3x² + 5 funksiyaning [-1; 3] kesmadagi eng katta qiymatini toping.", "5", "9", "1", "3", "A"),
    (2, "Integralni hisoblang: ∫₀^π sin(x) dx", "0", "1", "2", "π", "C"),
    (3, "f(x) = ln(x² - 2x + 2) funksiya hosilasining x = 2 nuqtadagi qiymatini f'(2) toping.", "1", "2", "0.5", "-1", "A"),
    (4, "Qutida 4 ta oq va 6 ta qora shar bor. Qutidan tavakkaliga ketma-ket (qaytarib salmasdan) 2 ta shar olindi. Ikkala sharning ham oq bo'lishi ehtimolligini (P) toping.", "4/25", "2/15", "1/3", "6/25", "B"),
    (5, "y = e^x va y = e^(-x) funksiya grafiklari hamda x = 1 to'g'ri chizig'i bilan chegaralangan shaklning yuzini toping.", "e + 1/e - 2", "e - 1/e", "e + 1/e", "2(e - 1)", "A"),
    (6, "f(x) = (x² - 3x + 2) / (x - 1) funksiyaning x → 1 dagi limitini hisoblang.", "1", "-1", "Limit mavjud emas", "0", "B"),
    (7, "Radiusi R bo'lgan sharga ichki chizilgan eng katta hajmli silindrning balandligi (h) nimaga teng bo'ladi?", "2R/√3", "R/√2", "R√3", "R√2", "A"),
    (8, "Tenglamani yeching: 3·9^x - 10·3^x + 3 = 0. Ildizlari ko'paytmasini toping.", "-1", "1", "0", "2", "A"),
    (9, "Konusning o'q kesimi to'g'ri burchakli uchburchakdan iborat. Agar konusning hajmi 9π sm³ bo'lsa, uning balandligini toping.", "3 sm", "2 sm", "√3 sm", "6 sm", "A"),
    (10, "z = 1 + i√3 kompleks sonning trigonometrik shaklini toping.", "2(cos(π/3) + i·sin(π/3))", "2(cos(π/6) + i·sin(π/6))", "√2(cos(π/4) + i·sin(π/4))", "√3(cos(π/3) + i·sin(π/3))", "A"),
    (11, "f(x) = 2·sin(x) - x funksiyaning [0; π] kesmadagi maksimum nuqtasini toping.", "x = π/3", "x = π/6", "x = π/2", "x = π/4", "A"),
    (12, "a va b birlik vektorlar bo'lib, ular orasidagi burchak 60° bo'lsa, |2a - b| vektorning modulini toping.", "√3", "1", "√5", "2", "A"),
    (13, "Tengsizlikni yeching: log_x(x + 2) > 1", "(1; +∞)", "(0; 1)", "(1; 2)", "(0; +∞)", "A"),
    (14, "To'g'ri chiziqli harakat qilayotgan nuqtaning tezlik qonuniyati v(t) = 3t² - 2t + 1 (m/s). Shu nuqtaning t = 0 dan t = 3 gacha bosib o'tgan yo'lini (S) toping.", "21 m", "19 m", "27 m", "24 m", "A"),
    (15, "x³ - 6x² + 11x - 6 = 0 tenglamaning eng katta va eng kichik ildizlari ayirmasini toping.", "1", "2", "3", "4", "B"),
    (16, "Muntazam tetraedrning qirrasi a ga teng. Uning to'la sirti yuzini toping.", "a²√3", "4a²√3", "a²√3 / 4", "2a²√3", "A"),
    (17, "Agar log₃5 = a va log₅7 = b bo'lsa, log₁₀₅(35) ifodani a va b orqali toping.", "(1 + a) / (1 + a + ab)", "(a + ab) / (1 + a + ab)", "(1 + b) / (1 + a + b)", "ab / (1 + a + ab)", "B"),
    (18, "Nishonga qarab 3 marta o'q uzildi. Har bir o'qning nishonga tegish ehtimolligi 0.8 ga teng. Nishonga kamida bir marta o'q tegish ehtimolligini toping.", "0.992", "0.512", "0.8", "0.96", "A"),
    (19, "y = √(4 - x²) funksiya grafigi ostida yotgan sohaning yuzini aniqlang.", "4π", "2π", "π", "3π", "B"),
    (20, "Agar f(x) = x·ln(x) bo'lsa, f''(e) (ikkinchi tartibli hosila) qiymatini toping.", "1/e", "1", "e", "e²", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=11, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=11,
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
    Test.objects.filter(title=TITLE, grade=11).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0047_seed_grade10_math_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
