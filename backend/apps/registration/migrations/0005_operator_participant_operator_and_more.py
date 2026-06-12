import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_participant_target_test_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='participant',
            name='self_referral',
            field=models.BooleanField(default=False, help_text="Mijoz operatorsiz, o'zi eshitib kelgan"),
        ),
        migrations.AddField(
            model_name='participant',
            name='operator',
            field=models.ForeignKey(blank=True, help_text='Mijozni olib kelgan operator', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='participants', to='registration.operator'),
        ),
    ]
