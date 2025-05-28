from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings


class Command(BaseCommand):
    help = "Create an admin user with credentials from .env"

    def handle(self, *args, **options):
        User = get_user_model()

        username = getattr(settings, "ADMIN_USERNAME", None)
        password = getattr(settings, "ADMIN_PASSWORD", None)
        email = getattr(settings, "ADMIN_EMAIL", None)

        if not all([username, password, email]):
            self.stderr.write(
                self.style.ERROR(
                    "ADMIN_USERNAME, ADMIN_PASSWORD, and ADMIN_EMAIL must be set in settings.py"
                )
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.NOTICE(f"Admin user '{username}' already exists.")
            )
        else:
            User.objects.create_superuser(
                username=username, password=password, email=email
            )
            self.stdout.write(self.style.SUCCESS(f"Admin user '{username}' created."))
