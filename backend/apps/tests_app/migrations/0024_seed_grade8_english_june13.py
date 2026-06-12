# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Ingliz tili 8-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Complete the sentence: \"By the time we get to the cinema, the movie ________.\"", "will start", "will have started", "starts", "started", "B"),
    (2, "Choose the correct COMPLEX OBJECT sentence:", "I want that he sings a song.", "I want him to sing a song.", "I want him sing a song.", "I want him singing a song.", "B"),
    (3, "Complete the sentence: \"I wish I ________ my project yesterday.\"", "finished", "had finished", "would finish", "have finished", "B"),
    (4, "Choose the correct inversion: \"Rarely ________ such a beautiful sunset.\"", "have I seen", "I have seen", "I saw", "I had seen", "A"),
    (5, "Which sentence shows the correct use of \"USED TO\"?", "I am used to living in Samarkand.", "I used to play football when I was a child.", "I get used to the hot weather here.", "I would use to play football as a child.", "B"),
    (6, "Complete the sentence: \"The report ________ by the committee by tomorrow evening.\"", "will be written", "will have been written", "is written", "would be written", "B"),
    (7, "Choose the correct option: \"It's high time you ________ studying for your exams.\"", "start", "started", "have started", "will start", "B"),
    (8, "Which is a synonym of \"ACCOMPLISH\" (erishmoq/bajarmoq)?", "Fail", "Achieve", "Abandon", "Attempt", "B"),
    (9, "Complete the sentence: \"Had I ________ about your arrival, I would have met you at the station.\"", "know", "knew", "known", "have known", "C"),
    (10, "What does the phrasal verb \"BREAK DOWN\" mean?", "To understand", "To stop working (machinery)", "To start a journey", "To break into pieces", "B"),
    (11, "Choose the correct tag question: \"Neither of them was late, ________?\"", "were they", "was it", "was he", "wasn't it", "A"),
    (12, "Complete the sentence: \"If only I ________ more money, I would travel around the world.\"", "had", "have", "would have", "had had", "A"),
    (13, "Complete the sentence: \"The news ________ so shocking that we couldn't believe it.\"", "are", "is", "were", "has been", "B"),
    (14, "Complete the sentence: \"She is ________ to win the competition.\"", "unlikely", "likely", "liking", "probably", "B"),
    (15, "Choose the correct causative structure: \"I ________ my hair ________ yesterday.\"", "had / cut", "have / cut", "had / cutting", "got / cutting", "A"),
    (16, "Which sentence is in the SUBJUNCTIVE MOOD?", "I recommend that he be present at the meeting.", "I know that he is present at the meeting.", "I think that he will be present at the meeting.", "I suggest that he is present at the meeting.", "A"),
    (17, "\"The building was pulled down.\" What does 'pulled down' mean?", "Built", "Demolished (buzib tashlangan)", "Painted", "Repaired", "B"),
    (18, "Complete the sentence: \"The teacher insists ________ the homework on time.\"", "on submitting", "at submitting", "to submit", "for submitting", "A"),
    (19, "Choose the correct pronoun: \"________ of the two brothers speaks English fluently.\"", "Both", "Each", "Neither", "Either", "B"),
    (20, "What does \"ON THE SPUR OF THE MOMENT\" mean?", "Carefully planned", "Without thinking, suddenly", "In a slow way", "At the right time", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Ingliz tili', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=8, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=8,
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
    Test.objects.filter(title=TITLE, grade=8).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0023_seed_grade7_english_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
