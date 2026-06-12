# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Ingliz tili 7-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Complete the sentence (Passive Voice): \"The new bridge ________ by the architect last year.\"", "was designed", "is designed", "has been designed", "had been designed", "A"),
    (2, "Complete the sentence in Reported Speech: \"He said, 'I am working on a new project now.'\"", "He said that he was working on a new project then.", "He said that he is working on a new project now.", "He said that he was working on a new project now.", "He said that he had been working on a new project then.", "A"),
    (3, "Choose the correct 3rd Conditional form: \"If I ________ about the meeting, I ________ earlier.\"", "knew / would come", "had known / would have come", "would know / had come", "had known / would come", "B"),
    (4, "Choose the correct phrasal verb: \"I need to ________ my essay before I submit it to the teacher.\"", "look for", "look after", "look over", "look into", "C"),
    (5, "Complete the sentence: \"Hardly ________ the lesson started when the bell rang.\"", "had", "did", "was", "were", "A"),
    (6, "Find the correct modal verb for logical deduction: \"He ________ be at home because his car is in the parking lot.\"", "must", "can't", "should", "might", "B"),
    (7, "\"Despite the heavy rain, they went out.\" Choose the best replacement for 'Despite':", "Although", "In spite of", "However", "Nevertheless", "B"),
    (8, "Choose the correct plural form of the word \"PHENOMENON\" (hodisa):", "Phenomenons", "Phenomena", "Phenomeni", "Phenomenas", "B"),
    (9, "Complete the sentence: \"I wish I ________ how to play the piano.\"", "know", "knew", "have known", "would know", "B"),
    (10, "Which sentence is grammatically INCORRECT?", "He suggested to go to the cinema.", "He suggested going to the cinema.", "He suggested that we go to the cinema.", "He suggested us going to the cinema.", "A"),
    (11, "Complete the sentence: \"You ________ do the dishes; I already did them.\"", "mustn't", "don't have to", "shouldn't", "needn't to", "B"),
    (12, "Choose the synonym of the word \"OBSTACLE\" (to'siq):", "Barrier", "Opportunity", "Advantage", "Challenge", "A"),
    (13, "Complete the sentence: \"She is looking forward to ________ you.\"", "meet", "meeting", "met", "have met", "B"),
    (14, "Complete the sentence: \"I ________ this book for three days, but I am only on page 50.\"", "have read", "have been reading", "read", "was reading", "B"),
    (15, "Choose the correct option: \"I would rather ________ at home tonight.\"", "to stay", "stay", "staying", "have stayed", "B"),
    (16, "Which of these is a DEPENDENT PREPOSITION?", "Interested in", "Fond of", "Both A and B are correct", "Neither A nor B", "C"),
    (17, "\"The cake was so delicious that I ate it all.\" What type of clause is this?", "Result clause", "Purpose clause", "Condition clause", "Comparison clause", "A"),
    (18, "Choose the correct word: \"The ________ of the new law caused a lot of discussion in parliament.\"", "introduction", "introduce", "introducing", "introduced", "A"),
    (19, "Complete the tag question: \"Let's go for a walk, ________?\"", "shall we", "don't we", "will we", "won't we", "A"),
    (20, "What does the phrasal verb \"CALL OFF\" mean?", "To postpone", "To cancel", "To visit someone", "To call again", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Ingliz tili', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=7, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=7,
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
    Test.objects.filter(title=TITLE, grade=7).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0022_seed_grade6_english_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
