# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Ingliz tili 5-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Complete the sentence: \"I lost my key yesterday, but look! I ________ it now.\"", "found", "have found", "find", "had found", "B"),
    (2, "Choose the correct sentence:", "This is the most baddest movie I have ever seen.", "This is the worst movie I have ever seen.", "This is the worse movie I have ever seen.", "This is the baddest movie I have ever seen.", "B"),
    (3, "Complete the sentence: \"The teacher gave us a lot of useful ________ before the exam.\"", "advices", "advice", "an advice", "informations", "B"),
    (4, "Choose the correct verb form: \"While my mother ________ dinner, the phone rang.\"", "was cooking", "cooked", "is cooking", "had cooked", "A"),
    (5, "Complete the sentence: \"We don't have ________ apples left. Let's buy some.\"", "much", "many", "some", "a few", "B"),
    (6, "Which word has the same form in singular and plural?", "Sheep", "Wolf", "Ox", "Mouse", "A"),
    (7, "Complete the sentence: \"This bicycle belongs to Tom. It is ________.\"", "his", "him", "he's", "its", "A"),
    (8, "Choose the correct preposition: \"We arrived ________ London ________ 4 o'clock in the afternoon.\"", "at / on", "in / at", "to / at", "in / in", "B"),
    (9, "Complete the sentence: \"Look at that boy! He is running too fast. He ________ fall down.\"", "will", "is going to", "does", "must", "B"),
    (10, "What do you call a person who designs houses and buildings?", "Engineer", "Builder", "Architect", "Planner", "C"),
    (11, "Choose the correct question tag: \"Lilly can speak French very well, ________?\"", "can she", "can't Lilly", "can't she", "isn't she", "C"),
    (12, "Complete the sentence: \"I am interested ________ learning new history facts.\"", "at", "in", "on", "for", "B"),
    (13, "Choose the correct spelling:", "Beautifully", "Beautifuly", "Beautifuly", "Beautifull", "A"),
    (14, "Complete the sentence: \"________ United Kingdom is an island country.\"", "A", "An", "The", "---", "C"),
    (15, "Choose the correct modal verb: \"You ________ touch that hot pan! You will burn your hand.\"", "shouldn't", "mustn't", "don't have to", "couldn't", "B"),
    (16, "Choose the correct sentence with the right word order:", "He always is late for his English lessons.", "He is always late for his English lessons.", "Always he is late for his English lessons.", "He is late always for his English lessons.", "B"),
    (17, "What is the opposite of the word \"FORGET\" (unutmoq)?", "Remember", "Remind", "Repeat", "Memorize", "A"),
    (18, "Complete the sentence: \"If it ________ tomorrow, we will stay at home.\"", "rain", "rains", "will rain", "rained", "B"),
    (19, "Choose the correct plural form for the word \"KNIFE\" (pichoq):", "knifes", "knives", "knifeth", "knife", "B"),
    (20, "Complete the question: \"________ does it take to get to school?\" — \"About 20 minutes.\"", "How much", "How far", "How long", "How many time", "C"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Ingliz tili', defaults={'is_active': True})

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
        ('tests_app', '0020_seed_grade4_english_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
