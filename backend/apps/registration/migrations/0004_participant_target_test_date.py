from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_participant_call_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='target_test_date',
            field=models.DateField(blank=True, help_text='Qaysi olimpiada kunida qatnashadi', null=True),
        ),
    ]
