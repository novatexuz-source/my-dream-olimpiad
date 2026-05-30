from django.db import migrations


def reset_admin(apps, schema_editor):
    from apps.users.models import User
    u, _ = User.objects.get_or_create(username='+998913769980')
    u.set_password('admin121')
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
