from django.db import migrations

TEST_TITLE = "1-sinf Ingliz tili: Advanced & Logic Test"

DATA = [
    (1, "Which spelling is CORRECT?", "Red", "Rde", "Erd", "A"),
    (2, "Look at the letters: 'o, b, o, k'. Rearrange them to make a school object.", "Book", "Desk", "Pen", "A"),
    (3, "Choose the correct word: 'An elephant is big, but a mouse is ......'", "tall", "small", "long", "B"),
    (4, "Complete the sentence: 'I ...... a student.'", "is", "am", "are", "B"),
    (5, "Find the ODD (ortiqcha) word in this group:", "Apple", "Banana", "Cat", "C"),
    (6, "What is the plural (ko'plik) form of the word 'CAT'?", "Cats", "Cates", "Catse", "A"),
    (7, "Which animal can FLY?", "A dog", "A fish", "A bird", "C"),
    (8, "Choose the opposite (teskari) word for 'HAPPY':", "Good", "Sad", "Big", "B"),
    (9, "Complete the phrase: 'Good ......, teacher!' (in the morning)", "morning", "afternoon", "evening", "A"),
    (10, "What color is the sky on a sunny day?", "Green", "Red", "Blue", "C"),
    (11, "Which letter is a VOWEL (unli harf)?", "B", "E", "T", "B"),
    (12, "Complete the dialogue: — 'How are you?' — '......, thank you.'", "I am six", "I am fine", "Goodbye", "B"),
    (13, "Choose the correct greeting when you meet a friend:", "Goodbye", "Hello", "Thank you", "B"),
    (14, "Which of these is NOT a color?", "Green", "Pen", "Yellow", "B"),
    (15, "How many days are there in a week? (In English)", "Five", "Six", "Seven", "C"),
    (16, "Complete the sentence: 'This is ...... apple.'", "a", "an", "two", "B"),
    (17, "Find the word that starts with the sound /b/:", "Pencil", "Ball", "Frog", "B"),
    (18, "What do you use to sit on in the classroom?", "A table", "A chair", "A board", "B"),
    (19, "Choose the correct spelling for the number 8:", "Eigt", "Eight", "Eigth", "B"),
    (20, "Complete the family member word: 'M_th_r'", "o / e", "a / e", "u / o", "A"),
]


def seed(apps, schema_editor):
    Subject = apps.get_model('tests_app', 'Subject')
    Test = apps.get_model('tests_app', 'Test')
    Question = apps.get_model('tests_app', 'Question')

    subject, _ = Subject.objects.get_or_create(name='Ingliz tili', defaults={'is_active': True})

    test, _ = Test.objects.get_or_create(
        subject=subject, grade=1, title=TEST_TITLE,
        defaults={'duration_minutes': 20, 'passing_percentage': 70.0, 'is_active': True},
    )

    if test.questions.exists():
        return

    for order, text, a, b, c, correct in DATA:
        Question.objects.create(
            test=test, order_number=order, question_text=text,
            option_a=a, option_b=b, option_c=c, option_d="", correct_answer=correct,
        )


def unseed(apps, schema_editor):
    Test = apps.get_model('tests_app', 'Test')
    Test.objects.filter(title=TEST_TITLE, grade=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0014_seed_grade11_math'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
