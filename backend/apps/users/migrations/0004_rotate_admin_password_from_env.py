import os

from django.db import migrations


def rotate_admin(apps, schema_editor):
    """Rotate the admin password on deploy when ADMIN_PASSWORD is set.

    The previous migrations shipped a hardcoded password in git history, so
    every production deployment MUST set ADMIN_USERNAME + ADMIN_PASSWORD env
    vars to replace it. If they are absent, the existing password is kept.
    """
    username = os.getenv('ADMIN_USERNAME', '+998913769980')
    password = os.getenv('ADMIN_PASSWORD')
    if not password:
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
        ('users', '0003_reset_admin_password'),
    ]

    operations = [
        migrations.RunPython(rotate_admin, noop),
    ]
