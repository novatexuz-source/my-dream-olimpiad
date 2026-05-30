from django.db import migrations

TEST_TITLE = "11-sinf: Geometriya va Matematika Aralash Test"

DATA = [
    (1, "Funksiyaning hosilasini toping: f(x) = x · ln(x) - x", "ln(x)", "ln(x) - 1", "1/x - 1", "A"),
    (2, "Radiusi 5 sm bo'lgan metall shar eritilib, balandligi 5 sm bo'lgan konus quyildi. Hosil bo'lgan konus asosining radiusini toping.", "10 sm", "5 sm", "5√2 sm", "A"),
    (3, "Integralni hisoblang: ∫ (0 dan 2 gacha) (3x² - 2x) dx", "4", "6", "8", "A"),
    (4, "To'g'ri silindrning o'q kesimi yuzi 24 sm² ga teng. Agar uning balandligi 6 sm bo'lsa, silindrning hajmini (V) toping (π o'zgarmas).", "24π sm³", "12π sm³", "48π sm³", "A"),
    (5, "f(x) = 2x³ - 9x² + 12x - 3 funksiyaning kamayish oralig'ini toping.", "(1; 2)", "(-∞; 1) ∪ (2; +∞)", "(2; 3)", "A"),
    (6, "Konusning yasovchisi 10 sm ga teng va u asos tekisligi bilan 45° li burchak hosil qiladi. Konusning yon sirti yuzini toping.", "50π√2 sm²", "50π sm²", "25π√2 sm²", "A"),
    (7, "y = x² parabola, x = 3 to'g'ri chiziq va y = 0 (abssissa o'qi) bilan chegaralangan egri chiziqli trapetsiyaning yuzini toping.", "9", "27", "3", "A"),
    (8, "Sharning hajmi 36π sm³ ga teng. Shu sharning sirti (sferaning yuzi) nechaga teng?", "36π sm²", "16π sm²", "24π sm²", "A"),
    (9, "Berilgan f(x) = sin²(x) funksiyaning boshlang'ich funksiyasini toping.", "x/2 - sin(2x)/4 + C", "x/2 + sin(2x)/4 + C", "-cos³(x)/3 + C", "A"),
    (10, "Silindr ichiga uning asoslariga va yon sirtiga urinadigan sfera chizilgan (teng tomonli silindr). Silindr hajmining sfera hajmiga bo'lgan nisbatini toping.", "3 : 2", "4 : 3", "2 : 1", "A"),
    (11, "f(x) = e^(2x) - 4x funksiyaning minimum nuqtasini (x_min) toping.", "ln(2)", "ln(2)/2", "0", "B"),
    (12, "Konus asosining radiusi 3 sm, hajmi esa 12π sm³. Shu konusning to'liq sirti yuzini toping.", "24π sm²", "15π sm²", "36π sm²", "A"),
    (13, "y = 2x + 1 to'g'ri chiziq y = x² + c parabolaga urinma bo'lsa, c ning qiymatini toping.", "2", "1", "3", "A"),
    (14, "Radiusi 13 sm bo'lgan shardan markazdan 5 sm masofada tekislik o'tkazilgan. Kesimda hosil bo'lgan doiraning yuzini toping.", "144π sm²", "169π sm²", "25π sm²", "A"),
    (15, "f(x) = (x²+1)/x funksiyaning [0.5; 2] kesmadagi eng katta qiymatini toping.", "2.5", "2", "3", "A"),
    (16, "Tomoni 6 sm bo'lgan kvadratni bitta tomoni atrofida aylantirishdan hosil bo'lgan jismning yon sirti yuzini toping.", "72π sm²", "36π sm²", "144π sm²", "A"),
    (17, "Qutida 3 ta oq va 7 ta qora shar bor. Tavakkaliga olingan 2 ta sharning ikkalasi ham qora bo'lish ehtimolligini toping.", "7/15", "21/100", "7/10", "A"),
    (18, "Kesik konus asoslarining radiuslari 3 sm va 6 sm, balandligi esa 4 sm. Kesik konusning yasovchisini (L) toping.", "5 sm", "5√2 sm", "6 sm", "A"),
    (19, "Jism v(t) = 3t² - 4t + 1 (m/s) tezlik qonuniyati bilan to'g'ri chiziqli harakat qilyapti. U t=0 dan t=3 soniyagacha qancha masofani (metr) bosib o'tadi?", "18 m", "12 m", "15 m", "B"),
    (20, "Sferaning radiusi 20% ga orttirilsa, uning hajmi necha foizga ortadi?", "72.8%", "44%", "60%", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Matematika', defaults={'is_active': True})

    test, _ = Test.objects.get_or_create(
        subject=subject, grade=11, title=TEST_TITLE,
        defaults={'duration_minutes': 60, 'passing_percentage': 70.0, 'is_active': True},
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
    Test.objects.filter(title=TEST_TITLE, grade=11).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0013_seed_grade10_math'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
