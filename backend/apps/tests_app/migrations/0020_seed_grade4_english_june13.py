# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Ingliz tili 4-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Complete the sentence: \"We ________ to Samarkand last summer and saw many historical places.\"", "go", "went", "gone", "have gone", "B"),
    (2, "Choose the correct superlative form: \"This is the ________ book in the school library.\"", "interestingest", "most interesting", "more interesting", "most interestingest", "B"),
    (3, "Complete the sentence: \"How ________ money do you need to buy this pencil case?\"", "many", "much", "any", "little", "B"),
    (4, "Choose the correct modal verb: \"The traffic light is red. You ________ stop!\"", "must", "should", "can", "might", "A"),
    (5, "Complete the sentence: \"He is a very good driver. He drives a car ________.\"", "careful", "carefully", "carefuly", "caringly", "B"),
    (6, "Choose the correct question for the underlined word: \"They played football in the park yesterday.\"", "When did they play football?", "Where did they play football?", "Why did they play football?", "How did they play football?", "B"),
    (7, "Find the plural form of the word \"TOOTH\" (tish):", "tooths", "teeth", "teeths", "toothes", "B"),
    (8, "Complete the sentence: \"While I was walking, I saw three ________ flying in the sky.\"", "gooses", "geese", "geeses", "goose", "B"),
    (9, "Choose the correct preposition: \"We usually have lunch ________ noon.\"", "at", "in", "on", "by", "A"),
    (10, "Complete the sentence: \"There are ________ pupils in the classroom, so it is very crowded.\"", "much", "too many", "too much", "a lot", "B"),
    (11, "Find the regular verb (oʻtgan zamonda -ed oladigan):", "Write", "Sleep", "Visit", "Buy", "C"),
    (12, "Complete the sentence: \"My friend ________ his homework yet. He is still working.\"", "hasn't finished", "didn't finish", "finished", "won't finish", "A"),
    (13, "Choose the correct spelling for the number 40:", "Fourty", "Forty", "Fortty", "Fourtty", "B"),
    (14, "Complete the sentence: \"This is ________ useful computer program.\"", "a", "an", "---", "the", "A"),
    (15, "What do we call the day BEFORE yesterday?", "Tomorrow", "The day after tomorrow", "The day before yesterday", "Last yesterday", "C"),
    (16, "Choose the correct pronouns: \"Tom and Lilly are my cousins. I like to play with ________.\"", "they", "them", "their", "theirs", "B"),
    (17, "Complete the sentence: \"Look at the sky! It is full of black clouds. It ________ rain.\"", "is going to", "will", "goes to", "is going", "A"),
    (18, "Choose the correct order of adjectives: \"She bought a ________ bag.\"", "beautiful small red", "red small beautiful", "small red beautiful", "small beautiful red", "A"),
    (19, "What is the opposite of the word \"POLITE\" (odobli)?", "Unpolite", "Impolite", "Dispolite", "Nonpolite", "B"),
    (20, "Choose the correct tag question: \"You don't like milk, ________?\"", "do you", "don't you", "you do", "aren't you", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Ingliz tili', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=4, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=4,
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
    Test.objects.filter(title=TITLE, grade=4).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0019_seed_grade3_english_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
