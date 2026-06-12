# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Ingliz tili 3-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Complete the sentence: \"Look! The children ________ football in the garden right now.\"", "play", "are playing", "is playing", "were playing", "B"),
    (2, "Choose the correct comparative form: \"An elephant is ________ than a horse.\"", "bigger", "more big", "biger", "more bigger", "A"),
    (3, "Complete the sentence: \"Whose bag is this? It's not my bag. It is ________.\"", "her", "hers", "she", "herself", "B"),
    (4, "Choose the correct sentence with the right order of words:", "We go usually to the park on Sunday.", "Usually we to the park go on Sunday.", "We usually go to the park on Sunday.", "We go to the park usually on Sunday.", "C"),
    (5, "Complete the sentence: \"My brother ________ like eating tomatoes. He hates them.\"", "doesn't", "don't", "isn't", "didn't", "A"),
    (6, "Find the plural form of the word \"MOUSE\":", "mouses", "mice", "mices", "mouse", "B"),
    (7, "Complete the sentence: \"Yesterday, I ________ a beautiful bird in the tree.\"", "see", "seed", "saw", "seen", "C"),
    (8, "Choose the correct preposition: \"My birthday is ________ October.\"", "on", "in", "at", "from", "B"),
    (9, "Choose the correct preposition for time: \"School starts ________ half past eight.\"", "at", "on", "in", "by", "A"),
    (10, "Complete the sentence: \"There isn't ________ milk in the fridge.\"", "some", "any", "a", "the", "B"),
    (11, "What is the opposite of the word \"HEAVY\"?", "Light", "Hard", "Weak", "Slim", "A"),
    (12, "Complete the question: \"________ do you clean your room?\" — \"On Saturdays.\"", "What", "Where", "When", "How often", "C"),
    (13, "Choose the correct article: \"Cairo is the capital of ________ Egypt.\"", "a", "an", "---", "the", "C"),
    (14, "Complete the sentence: \"Tom is very good ________ drawing pictures.\"", "at", "in", "on", "for", "A"),
    (15, "Which animal is the TALLEST in the world?", "Elephant", "Giraffe", "Hippo", "Camel", "B"),
    (16, "Choose the correct spelling:", "Wednesday", "Wensday", "Wednesdaey", "Wedensday", "A"),
    (17, "Complete the sentence: \"Listen! Somebody ________ beautiful songs.\"", "sings", "is singing", "sing", "was singing", "B"),
    (18, "Choose the correct plural form for \"WOLF\":", "wolfs", "wolves", "wolvies", "wolfes", "B"),
    (19, "What do you call a person who flies a plane?", "Doctor", "Driver", "Pilot", "Engineer", "C"),
    (20, "Choose the correct answer: \"Whose pencils are these?\"", "They are Tom's.", "It is Tom's.", "They are Toms.", "Their are Tom's.", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Ingliz tili', defaults={'is_active': True})

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
        ('tests_app', '0018_seed_grade2_english_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
