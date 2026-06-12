# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import migrations

TZ = ZoneInfo('Asia/Tashkent')
TITLE = "Ingliz tili 10-sinf (13.06.2026)"
START = datetime(2026, 6, 13, 8, 0, tzinfo=TZ)
END = datetime(2026, 6, 13, 16, 0, tzinfo=TZ)

# (order, question_text, option_a, option_b, option_c, option_d, correct_answer)
DATA = [
    (1, "Complete the sentence: \"Little ________ about the plans we had made.\"", "did he know", "he knew", "knew he", "he did know", "A"),
    (2, "Choose the correct sentence (Subjunctive Mood – past regret):", "I wish I have known the truth back then.", "I wish I had known the truth back then.", "I wish I would have known the truth back then.", "I wish I knew the truth back then.", "B"),
    (3, "Complete the sentence: \"It's high time the government ________ the corruption issue.\"", "tackled", "tackles", "should tackle", "would tackle", "A"),
    (4, "Complete the sentence: \"Should you ________ any assistance, please do not hesitate to contact us.\"", "need", "needed", "would need", "have needed", "A"),
    (5, "Which sentence uses the correct order of adjectives?", "A gorgeous old Italian silk scarf.", "A silk gorgeous old Italian scarf.", "An old gorgeous Italian silk scarf.", "An Italian old gorgeous silk scarf.", "A"),
    (6, "Complete the sentence: \"By the time the performance finishes, the orchestra ________ for four hours.\"", "will have played", "will have been playing", "is playing", "would have been playing", "B"),
    (7, "Complete the sentence: \"Despite ________ wealthy, he lived a modest life.\"", "his being", "he was", "him being", "to be", "A"),
    (8, "Which word is a synonym for \"VACILLATE\" (ikkilanmoq)?", "Hesitate", "Decide", "Persist", "Accelerate", "A"),
    (9, "Complete the sentence: \"Never ________ such an arrogant display of power.\"", "have I seen", "I have seen", "did I see", "had I seen", "A"),
    (10, "Complete the sentence: \"I'd sooner you ________ me in cash.\"", "paid", "pay", "would pay", "had paid", "A"),
    (11, "Choose the correct causative: \"I ________ my house ________ last summer.\"", "had / repainted", "have / repainted", "had / repainting", "had / to repaint", "A"),
    (12, "Complete the sentence: \"They ________ by now, but the flight was delayed.\"", "should have arrived", "should arrive", "should be arriving", "must have arrived", "A"),
    (13, "Complete the sentence: \"Not only ________ five languages, but she is also an expert in quantum physics.\"", "does she speak", "she speaks", "speaks she", "she does speak", "A"),
    (14, "What is the meaning of the idiom \"TO BE ON THE BREADLINE\"?", "To be very wealthy", "To be extremely poor", "To work in a bakery", "To eat only bread", "B"),
    (15, "Complete the sentence: \"________ been warned several times, he finally apologized.\"", "Having", "Had", "Having been", "Been", "C"),
    (16, "Which of the following is NOT an inversion?", "Under no circumstances will I sign this.", "So fast did he run that he won the race.", "He ran so fast that he won the race.", "Rarely does he miss a meeting.", "C"),
    (17, "Complete the sentence: \"The decision is ________ ________ the final results.\"", "contingent / on", "dependent / of", "contingent / of", "reliant / about", "A"),
    (18, "Complete the sentence: \"The audience ________ clapping for ten minutes.\"", "was", "were", "is", "has been", "B"),
    (19, "Complete the sentence: \"Were ________ more diligent, he would have succeeded.\"", "he to be", "he", "he had been", "he be", "A"),
    (20, "What is the subtle meaning of \"I could have done better\"?", "I did my best but failed.", "I achieved a good result, but it wasn't my maximum.", "I didn't try at all.", "I regret not doing it at all.", "B"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Ingliz tili', defaults={'is_active': True})

    if Test.objects.filter(subject=subject, grade=10, start_datetime__date=START.date()).exists():
        return

    test = Test.objects.create(
        subject=subject,
        grade=10,
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
    Test.objects.filter(title=TITLE, grade=10).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0025_seed_grade9_english_june13'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
