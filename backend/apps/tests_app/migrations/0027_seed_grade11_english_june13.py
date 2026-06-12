# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Ingliz tili 11-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Complete the sentence: \"By the time the committee submits the final report, they ________ the data for over six months.\"", "will analyze", "will have been analyzing", "are analyzing", "will have analyzed", "B"),
    (2, "Choose the correct form: \"It is essential that he ________ present at the grand opening.\"", "be", "is", "will be", "would be", "A"),
    (3, "Complete the sentence: \"I'd rather you ________ the results of the test to the media yesterday.\"", "didn't disclose", "hadn't disclosed", "wouldn't disclose", "wouldn't have disclosed", "B"),
    (4, "Complete the sentence: \"No sooner ________ the stage than the audience erupted into applause.\"", "had the singer stepped", "the singer had stepped", "did the singer stepped", "the singer has stepped", "A"),
    (5, "Complete the sentence: \"The company's success is ________ on the approval of the new budget.\"", "contingent", "relevant", "capable", "insistent", "A"),
    (6, "Complete the sentence: \"I object to ________ like a child in this office.\"", "be treated", "treating", "being treated", "treated", "C"),
    (7, "Which word is a synonym for \"METICULOUS\" (o'ta sinchkov/daqiqa)?", "Careless", "Scrupulous", "Superficial", "Negligent", "B"),
    (8, "Complete the sentence: \"Under no circumstances ________ you leave the examination room before the bell.\"", "you should", "should you", "did you", "should you not", "B"),
    (9, "Complete the sentence: \"________ being very tired, she managed to finish the presentation on time.\"", "Despite", "Although", "However", "Even though", "A"),
    (10, "What does the idiom \"TO BURN THE MIDNIGHT OIL\" mean?", "To waste energy", "To study or work late into the night", "To cook a late-night meal", "To argue fiercely", "B"),
    (11, "Choose the grammatically CORRECT sentence:", "He suggested to take a break.", "He suggested taking a break.", "He suggested us to take a break.", "He suggested that we to take a break.", "B"),
    (12, "Complete the sentence: \"I am looking forward to ________ your feedback regarding the proposal.\"", "receive", "receiving", "have received", "to have received", "B"),
    (13, "Complete the sentence: \"If it ________ for his financial support, the project would have failed last year.\"", "weren't", "hadn't been", "wouldn't be", "wasn't", "B"),
    (14, "Choose the correct spelling for the word that means 'tasodifiy uchrashuv':", "Encounter", "Enconter", "Encownter", "Incownter", "A"),
    (15, "Complete the sentence: \"The news ________ so overwhelming that we had to take a moment to process it.\"", "was", "were", "are", "has been", "A"),
    (16, "Complete the tag question: \"Seldom do we see such dedication, ________?\"", "don't we", "do we", "isn't it", "aren't we", "B"),
    (17, "What is the antonym of the word \"OBSTINATE\" (o'jar/qaysar)?", "Stubborn", "Flexible", "Persistent", "Determined", "B"),
    (18, "Complete the sentence: \"________ completed the grueling assignment, he felt a huge sense of relief.\"", "Having", "Had", "After he has", "While", "A"),
    (19, "Choose the correct order of adjectives:", "An antique beautiful leather jacket.", "A beautiful antique leather jacket.", "A leather beautiful antique jacket.", "A antique beautiful leather jacket.", "B"),
    (20, "What does the phrasal verb \"LOOK UP TO\" mean?", "To search for something online", "To admire and respect someone", "To physically look upwards", "To feel superior to someone", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Ingliz tili', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=11, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=11,
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
    Test.objects.filter(title=TITLE, grade=11).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0026_seed_grade10_english_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
