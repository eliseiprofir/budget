from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

DEFAULT_EMAIL = "root@root.com"
DEFAULT_PASSWORD = "root"

User = get_user_model()


class Command(BaseCommand):
    help = f"""Create a default superuser with predefined credentials.\n
    Email: {DEFAULT_EMAIL}\n
    Password: {DEFAULT_PASSWORD}"""

    def handle(self, *args, **options):
        if not User.objects.filter(email=DEFAULT_EMAIL).exists():
            User.objects.create_superuser(
                email=DEFAULT_EMAIL,
                password=DEFAULT_PASSWORD,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Default superuser created successfully!\
                                                 \nEmail: {DEFAULT_EMAIL}\
                                                 \nPassword: {DEFAULT_PASSWORD}"),
            )
            return

        self.stdout.write(
            self.style.WARNING(f"Default superuser already exists.\
                                                \nEmail: {DEFAULT_EMAIL}\
                                                \nPassword: {DEFAULT_PASSWORD}"),
        )
        return
