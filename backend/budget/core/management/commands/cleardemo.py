from django.core.management.base import BaseCommand
from model_bakery import baker  #noqa F401

from accounts.models import User
from core.models import Location
from core.models import Bucket
from transactions.models import Category
from transactions.models import Transaction

from .seeddemo import USER_EMAIL


class Command(BaseCommand):
    help = """Clears the database entries except for superusers."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-input",
            action="store_true",
            dest="no_input",
            help="Delete without asking for confirmation",
        )

    def handle(self, *args, **options):
        # Count records to be deleted
        user = User.all_objects.filter(email=USER_EMAIL).first()

        if user is None:
            self.stdout.write(self.style.ERROR("No demo user was found."))
            return
        
        location_count = Location.all_objects.filter(user=user).count()
        bucket_count = Bucket.all_objects.filter(user=user).count()
        category_count = Category.all_objects.filter(user=user).count()
        transaction_count = Transaction.objects.filter(user=user).count()

        total_count = (
            1 +
            location_count + bucket_count +
            category_count + transaction_count
        )

        # Show summary of all what will be deleted
        self.stdout.write(self.style.WARNING(f"""
You are about to delete the following records from the database:
- {user.email} user
- {location_count} locations
- {bucket_count} buckets
- {category_count} categories
- {transaction_count} transactions
- TOTAL records to be deleted: {total_count}
"""))

        should_proceed = True
        if not options.get("no_input", False):
            confirm = input("Are you sure you want to delete all these records? [y/N]: ")
            should_proceed = confirm.lower() == "y"

        if not should_proceed:
            self.stdout.write(self.style.SUCCESS("\nOperation cancelled."))
            return

        # Proceed with deletion
        self.stdout.write("\nDeleting records...")

        User.all_objects.filter(email=USER_EMAIL).delete()
        self.stdout.write(self.style.NOTICE("✓ Users deleted (excluding superusers)"))

        Location.all_objects.filter(user=user).delete()
        self.stdout.write(self.style.NOTICE("✓ Locations deleted"))

        Bucket.all_objects.filter(user=user).delete()
        self.stdout.write(self.style.NOTICE("✓ Buckets deleted"))

        Category.all_objects.filter(user=user).delete()
        self.stdout.write(self.style.NOTICE("✓ Categories deleted"))

        Transaction.objects.filter(user=user).delete()
        self.stdout.write(self.style.NOTICE("✓ Transactions deleted"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully deleted {total_count} records from the database.\n",
            ),
        )
