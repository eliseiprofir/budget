from django.core.management.base import BaseCommand
from model_bakery import baker

class Command(BaseCommand):
    help = """Clears the database entries except for superusers."""

    