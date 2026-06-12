# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Ingliz tili 6-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Complete the sentence: \"I ________ this book for three hours, but I haven't finished it yet.\"", "read", "am reading", "have been reading", "have read", "C"),
    (2, "Choose the correct word: \"The teacher asked us to be quiet because the students ________ an important test.\"", "wrote", "were writing", "have written", "are writing", "B"),
    (3, "Choose the correct phrasal verb: \"It's very cold outside. Make sure you ________ your warm jacket.\"", "put on", "take off", "turn on", "put up", "A"),
    (4, "Fill in the blank: \"I don't like this soup. There is ________ salt in it.\"", "too many", "too much", "enough many", "very much", "B"),
    (5, "Complete the sentence: \"Lilly sings very ________, she should become a professional singer.\"", "good", "well", "beautiful", "nicely", "B"),
    (6, "Find the correct preposition: \"We are going on holiday ________ the end of July.\"", "in", "on", "at", "by", "C"),
    (7, "Choose the correct option: \"I haven't seen my uncle ________ 2024.\"", "for", "since", "from", "ago", "B"),
    (8, "What is the vocabulary definition of a person who is \"generous\"?", "A person who doesn't like to share things.", "A person who loves giving money or gifts to help others.", "A person who easily gets angry.", "A person who works very hard.", "B"),
    (9, "Complete the sentence with the correct reflexive pronoun: \"Don't worry about us, mom! We can cook dinner by ________.\"", "ourselves", "yourselves", "themselves", "oneself", "A"),
    (10, "Choose the correct spelling for the job:", "Businessmann", "Businessman", "Bisnesman", "Buisnessman", "B"),
    (11, "Choose the correct article: \"My brother plays ________ guitar, and my father plays ________ football.\"", "the / the", "the / ---", "--- / the", "a / ---", "B"),
    (12, "Complete the idiom: \"Don't worry about the exam! It's a piece of ________.\"", "cake", "bread", "apple", "pie", "A"),
    (13, "Choose the correct sentence with the right adjective order:", "He bought a modern big black car.", "He bought a big modern black car.", "He bought a black big modern car.", "He bought a big black modern car.", "B"),
    (14, "Complete the sentence: \"This is the ________ mountain I have ever climbed.\"", "most highest", "highest", "higher", "most high", "B"),
    (15, "What is the opposite of the word \"SHARP\" (o'tkir pichoqqa nisbatan)?", "Blunt", "Soft", "Weak", "Round", "A"),
    (16, "Choose the correct modal verb: \"You ________ bring your passport. The museum entry is free and they don't check IDs.\"", "mustn't", "don't have to", "shouldn't", "can't", "B"),
    (17, "Complete the sentence: \"If she ________ hard, she will pass the English competition.\"", "study", "studies", "will study", "studied", "B"),
    (18, "Choose the correct plural form of the word \"OASIS\" (voha):", "oasises", "oasies", "oases", "oasis", "C"),
    (19, "Choose the correct question tag: \"There is some milk left in the fridge, ________?\"", "isn't it", "isn't there", "is there", "aren't there", "B"),
    (20, "What do you call a collective group of wolves?", "A pack of wolves", "A herd of wolves", "A flock of wolves", "A pride of wolves", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Ingliz tili', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=6, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=6,
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
    Test.objects.filter(title=TITLE, grade=6).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0021_seed_grade5_english_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
