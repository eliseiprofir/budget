from django.core.management.base import BaseCommand
from model_bakery import baker

NO_OF_LOCATIONS = 5
NO_OF_BUCKETS = 5
NO_OF_POSITIVE_CATEGORIES = 2
NO_OF_NEGATIVE_CATEGORIES = 5
NO_OF_POSITIVE_TRANSACTIONS = 10
NO_OF_NEGATIVE_TRANSACTIONS = 25


class Command(BaseCommand):
    help = """Create multiple random entries in the database using bakery."""

    def handle(self, *args, **options):
        ...
