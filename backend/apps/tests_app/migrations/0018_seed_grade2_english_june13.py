# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Ingliz tili 2-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Choose the correct plural form (to'g'ri ko'plik shaklini toping):", "childs", "children", "childrens", "childes", "B"),
    (2, "Complete the sentence: \"Look at ________ birds up there in the sky!\"", "this", "these", "those", "that", "C"),
    (3, "Find the odd word out (guruhga kirmaydigan ortiqcha so'zni toping):", "Cucumber", "Apple", "Banana", "Orange", "A"),
    (4, "Complete the sentence: \"An elephant ________ got big ears.\"", "have", "has", "is", "do", "B"),
    (5, "Which day comes after Friday? (Juma kunidan keyin qaysi kun keladi?)", "Thursday", "Saturday", "Sunday", "Monday", "B"),
    (6, "Choose the correct spelling (to'g'ri yozilgan so'zni toping):", "Beautiful", "Beatiful", "Beautifull", "Beutiful", "A"),
    (7, "Where does a monkey live? (Maymun qayerda yashaydi?)", "In the sea", "In the jungle", "On the farm", "In the desert", "B"),
    (8, "Complete the dialogue: — \"How old are you?\" — \"________\"", "I'm fine, thank you.", "I'm eight years old.", "I'm a student.", "I'm from Uzbekistan.", "B"),
    (9, "Choose the opposite of \"BIG\" (teskari ma'nosini toping):", "Small", "Tall", "Long", "Wide", "A"),
    (10, "What is 5 + 4? Write in words:", "Eight", "Nine", "Ten", "Seven", "B"),
    (11, "Which fruit is yellow and sour (achchiq/nordon)?", "Lemon", "Strawberry", "Orange", "Banana", "A"),
    (12, "Complete the sentence: \"I ________ ride a bike, but I can't fly.\"", "am", "can", "can't", "do", "B"),
    (13, "Find the action verb (harakat bildirgan fe'lni toping):", "Happy", "Run", "Table", "Blue", "B"),
    (14, "Complete the sentence: \"This is ________ orange book.\"", "a", "an", "two", "the", "B"),
    (15, "Choose the correct plural form for \"BOX\" (quti):", "boxs", "boxes", "boxies", "box", "B"),
    (16, "Which room do you sleep in? (Qaysi xonada uxlaysiz?)", "Kitchen", "Bathroom", "Bedroom", "Living room", "C"),
    (17, "Complete the sentence: \"My mother's sister is my ________.\"", "aunt", "uncle", "grandmother", "cousin", "A"),
    (18, "What is the weather like when it snows? (Qor yog'ganda ob-havo qanday bo'ladi?)", "Hot", "Cold", "Sunny", "Warm", "B"),
    (19, "Look at the picture clue: \U0001F6CB What is this?", "Armchair", "Sofa", "Bed", "Chair", "B"),
    (20, "Choose the correct short answer: \"Can cats swim?\"", "Yes, they can.", "No, they can't.", "No, it can't.", "Yes, it can.", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Ingliz tili', defaults={'is_active': True})

    # Skip if a test already exists for this subject+grade on this date.
    if Test.objects.filter(subject=subject, grade=2, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=2,
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
    Test.objects.filter(title=TITLE, grade=2).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0017_seed_grade1_english_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
