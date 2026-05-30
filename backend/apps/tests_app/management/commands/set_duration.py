"""
Set the time limit (duration_minutes) for ALL tests at once.

Default: 20 minutes. You can pass a different number:
    python manage.py set_duration            # -> 20 minutes
    python manage.py set_duration --minutes 30
"""
from django.core.management.base import BaseCommand
from apps.tests_app.models import Test


class Command(BaseCommand):
    help = "Set duration_minutes for all tests (default 20)."

    def add_arguments(self, parser):
        parser.add_argument("--minutes", type=int, default=20)

    def handle(self, *args, **options):
        minutes = options["minutes"]
        updated = Test.objects.update(duration_minutes=minutes)
        self.stdout.write(self.style.SUCCESS(
            f"OK: {updated} ta testning vaqti {minutes} daqiqa qilib o'rnatildi."
        ))
