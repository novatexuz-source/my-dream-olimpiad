"""Set duration_minutes to 20 for ALL existing tests."""
from django.db import migrations


def set_all_to_20(apps, schema_editor):
    Test = apps.get_model('tests_app', 'Test')
    Test.objects.update(duration_minutes=20)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0015_seed_grade1_english'),
    ]

    operations = [
        migrations.RunPython(set_all_to_20, noop),
    ]
