# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Ingliz tili 1-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Choose the first letter of the English alphabet:", "B", "A", "Z", "C", "B"),
    (2, "What color is the sun? (Quyosh qaysi rangda?)", "Red", "Blue", "Yellow", "Green", "C"),
    (3, "Find the animal that says \"Meow\":", "Dog", "Cat", "Frog", "Cow", "B"),
    (4, "Count the stars: \U0001F31F \U0001F31F \U0001F31F \U0001F31F. How many?", "Three", "Four", "Five", "Two", "B"),
    (5, "Complete the greeting: \"Hello! What is your ... ?\"", "name", "book", "apple", "dog", "A"),
    (6, "Which word starts with the letter \"B\"?", "Apple", "Banana", "Cat", "Dog", "B"),
    (7, "Find the school object (maktab qurolini toping):", "Pen", "Milk", "Car", "Cat", "A"),
    (8, "What color is a frog? (Baqa qaysi rangda?)", "Green", "Pink", "Orange", "Blue", "A"),
    (9, "Choose the correct small letter for \"G\":", "q", "d", "g", "p", "C"),
    (10, "\"Good ...\" (Ertalab ko'rishganda nima deyiladi?)", "Night", "Morning", "Goodbye", "Bye", "B"),
    (11, "Find the odd word (ortiqcha so'zni toping):", "One", "Two", "Red", "Three", "C"),
    (12, "Which animal can fly (ucha oladi)?", "Fish", "Bird", "Lion", "Dog", "B"),
    (13, "What is this? \U0001F34E", "It is an apple.", "It is a banana.", "It is an orange.", "It is a lemon.", "A"),
    (14, "Complete the numbers: One, Two, Three, ...", "Five", "Four", "Six", "Ten", "B"),
    (15, "What color is a tomato?", "Red", "White", "Black", "Blue", "A"),
    (16, "Choose the letter that comes AFTER \"M\" (M harfidan keyin keladigan harf):", "L", "N", "O", "A", "B"),
    (17, "Find the family member (oila a'zosini toping):", "Teacher", "Mother", "Friend", "Doctor", "B"),
    (18, "What do we say when we sleep? (Yotishdan oldin nima deyiladi?)", "Good morning", "Good afternoon", "Good night", "Hello", "C"),
    (19, "How do you say \"rahmat\" in English?", "Please", "Thank you", "Sorry", "Hello", "B"),
    (20, "Unscramble the letters to find a toy: O, D, L, L.", "Doll", "Ball", "Car", "Train", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Ingliz tili', defaults={'is_active': True})

    # Skip if a test already exists for this subject+grade on this date.
    if Test.objects.filter(subject=subject, grade=1, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=1,
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
    Test.objects.filter(title=TITLE, grade=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0016_set_all_tests_20min'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
