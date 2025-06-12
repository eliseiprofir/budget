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

        # Proceed with deletion
        self.stdout.write("\nDeleting records...")

        User.all_objects.filter(email=USER_EMAIL).delete()
        self.stdout.write(self.style.NOTICE(f"✓ {user.email} user deleted"))

        Location.all_objects.filter(user=user).delete()
        self.stdout.write(self.style.NOTICE(f"✓ {location_count} Locations deleted"))

        Bucket.all_objects.filter(user=user).delete()
        self.stdout.write(self.style.NOTICE(f"✓ {bucket_count} Buckets deleted"))

        Category.all_objects.filter(user=user).delete()
        self.stdout.write(self.style.NOTICE(f"✓ {category_count} Categories deleted"))

        Transaction.objects.filter(user=user).delete()
        self.stdout.write(self.style.NOTICE(f"✓ {transaction_count} Transactions deleted"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully deleted {total_count} records from the database.\n",
            ),
        )
