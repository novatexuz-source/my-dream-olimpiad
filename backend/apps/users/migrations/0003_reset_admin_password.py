import os

from django.db import migrations


def reset_admin(apps, schema_editor):
    """Historical migration, rewritten to drop the hardcoded password.

    Only acts when ADMIN_USERNAME and ADMIN_PASSWORD env vars are provided.
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
    u.is_active = True
    u.role = 'super_admin'
    u.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_create_admin'),
    ]

    operations = [
        migrations.RunPython(reset_admin, noop),
    ]
