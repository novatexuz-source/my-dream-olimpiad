import os

from django.db import migrations


def create_admin(apps, schema_editor):
    """Create the initial admin from env vars (ADMIN_USERNAME / ADMIN_PASSWORD).

    Credentials must never be hardcoded in version control. If the env vars
    are not set, nothing is created — use `python manage.py createsuperuser`.
    """
    username = os.getenv('ADMIN_USERNAME')
    password = os.getenv('ADMIN_PASSWORD')
    if not username or not password:
        return

    from apps.users.models import User
    u, _ = User.objects.get_or_create(username=username)
    u.set_password(password)
    u.is_staff = True
    u.is_superuser = True
    u.role = 'super_admin'
    u.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin, noop),
    ]
