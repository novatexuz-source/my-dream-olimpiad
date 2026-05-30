from django.db import migrations

TEST_TITLE = "3-sinf Matematika: Murakkablashtirilgan Mantiqiy Test"


def fix(apps, schema_editor):
    Test = apps.get_model('tests_app', 'Test')
    test = Test.objects.filter(title=TEST_TITLE, grade=3).first()
    if not test:
        return
    q = test.questions.filter(order_number=12).first()
    if not q:
        return
    q.question_text = "Onasi 36 yoshda, qizi esa 10 yoshda. Necha yildan keyin onasi qizidan 3 barobar katta bo'ladi?"
    q.option_a = "3 yildan keyin"
    q.option_b = "4 yildan keyin"
    q.option_c = "5 yildan keyin"
    q.option_d = ""
    q.correct_answer = "A"
    q.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0005_seed_grade3_math'),
    ]

    operations = [
        migrations.RunPython(fix, noop),
    ]
