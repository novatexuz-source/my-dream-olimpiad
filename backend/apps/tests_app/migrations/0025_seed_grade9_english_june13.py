# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Ingliz tili 9-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Complete the sentence: \"If I ________ you, I ________ that job offer last month.\" (Mixed Conditional)", "were / would take", "had been / would have taken", "had been / would take", "were / would have taken", "C"),
    (2, "Choose the correct COMPLEX OBJECT structure: \"I remember ________ the door when I left.\"", "to lock", "locking", "having locked", "to have locked", "B"),
    (3, "Complete the sentence: \"Scarcely ________ into the room when the phone started ringing.\"", "had he walked", "he had walked", "did he walked", "has he walked", "A"),
    (4, "Choose the correct causative structure: \"The king had his subjects ________ a new palace.\"", "to build", "build", "building", "built", "B"),
    (5, "Complete the sentence: \"It's high time we ________ wasting our time on trivial things.\"", "stopped", "stop", "have stopped", "will stop", "A"),
    (6, "Which word is NOT a synonym of \"PERSISTENT\" (matonatli)?", "Determined", "Tenacious", "Vacillating", "Resolute", "C"),
    (7, "Complete the sentence: \"Despite ________ hard, she didn't succeed.\"", "have worked", "working", "to work", "worked", "B"),
    (8, "Complete the tag question: \"Nobody called the police, ________?\"", "did they", "didn't they", "did he", "called they", "A"),
    (9, "Choose the correct form: \"The ________ of the Alps ________ breathtaking.\"", "scenery / is", "sceneries / are", "scenery / are", "sceneries / is", "A"),
    (10, "\"The project was carried out successfully.\" What does 'carried out' mean?", "Conducted/Executed", "Abandoned", "Postponed", "Reported", "A"),
    (11, "Complete the sentence: \"I'd rather you ________ anyone about our plans.\"", "didn't tell", "wouldn't tell", "hadn't told", "don't tell", "A"),
    (12, "Choose the correct option: \"Little ________ about the surprise we prepared for him.\"", "did he know", "he knew", "knew he", "he did know", "A"),
    (13, "Which of these words is a 'false friend' (ma'nosi chalgʻitadigan so'z)?", "Actual (aslida / haqiqiy)", "Library", "Fabric", "Magazine", "A"),
    (14, "Complete the sentence: \"He is ________ to continue the race.\"", "too tired", "enough tired", "tired enough", "so tired", "A"),
    (15, "\"I should have done it differently.\" What does this express?", "Past obligation", "Past regret/criticism", "Future possibility", "Present ability", "B"),
    (16, "Which sentence is correctly punctuated?", "Although it was raining, but we went out.", "Although it was raining, we went out.", "Although it was raining we went out.", "But it was raining, although we went out.", "B"),
    (17, "Choose the correct option: \"He acts ________ he owns the company.\"", "as if", "as though", "Both A and B are correct", "like if", "C"),
    (18, "What is the meaning of \"TO BE ON THE BALL\"?", "To be very alert and prepared", "To be lazy", "To play sports", "To be in trouble", "A"),
    (19, "Complete the sentence: \"By the end of this year, I ________ English for ten years.\"", "will have studied", "will have been studying", "will study", "have been studying", "B"),
    (20, "Which sentence uses the Subjunctive Mood correctly?", "It is essential that every student be on time.", "It is essential that every student is on time.", "It is essential that every student will be on time.", "It is essential that every student should be on time.", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Ingliz tili', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=9, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=9,
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
    Test.objects.filter(title=TITLE, grade=9).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0024_seed_grade8_english_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
