import random
from django.core.management.base import BaseCommand
from model_bakery import baker
from itertools import cycle
from datetime import datetime
from django.utils.timezone import make_aware

from accounts.models import User
from transactions.models import Category

user_recipe = "accounts.tests.user_recipe"
location_recipe = "core.tests.location_recipe"
bucket_recipe = "core.tests.bucket_recipe"
positive_category_recipe = "transactions.tests.positive_category_recipe"
positive_transaction_recipe = "transactions.tests.positive_transaction_recipe"
negative_category_recipe = "transactions.tests.negative_category_recipe"
negative_transaction_recipe = "transactions.tests.negative_transaction_recipe"
neutral_category_recipe = "transactions.tests.neutral_category_recipe"
neutral_transaction_recipe = "transactions.tests.neutral_transaction_recipe"

USER_EMAIL = "test@test.com"
USER_PASSWORD = "test"

NO_OF_LOCATIONS = 5
NO_OF_BUCKETS = 5
NO_OF_POSITIVE_CATEGORIES = 2
NO_OF_NEGATIVE_CATEGORIES = 5
NO_OF_NEUTRAL_CATEGORIES = 1
NO_OF_POSITIVE_TRANSACTIONS = 20
NO_OF_NEGATIVE_TRANSACTIONS = 100
NO_OF_NEUTRAL_TRANSACTIONS = 5

TOTAL_ENTRIES_CREATED = (
    1 + NO_OF_LOCATIONS + NO_OF_BUCKETS +
    NO_OF_POSITIVE_CATEGORIES + NO_OF_POSITIVE_TRANSACTIONS +
    NO_OF_NEGATIVE_CATEGORIES + NO_OF_NEGATIVE_TRANSACTIONS +
    NO_OF_NEUTRAL_CATEGORIES + NO_OF_NEUTRAL_TRANSACTIONS
)

YEARS = [2022, 2023, 2024]
MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


class Command(BaseCommand):
    help = """Create multiple random entries in the database using bakery."""

    def handle(self, *args, **options):
        # Create user
        self.stdout.write(self.style.NOTICE("\nCreating user..."))

        try:
            user = User.objects.create_user(
            email=USER_EMAIL,
            password=USER_PASSWORD,
            full_name="Test User"
        )
        except Exception:
            self.stdout.write(self.style.ERROR("You already used 'seed' command before. If you want to use it again, run the 'clear' command first."))
            return

        # Create locations
        self.stdout.write(self.style.NOTICE("\nCreating locations..."))
        locations = []
        for _ in range(NO_OF_LOCATIONS):
            location = baker.make_recipe(location_recipe, user=user)
            locations.append(location)
            self.stdout.write(f"Created location: {location}")
        locations = cycle(locations)

        # Create buckets
        self.stdout.write(self.style.NOTICE("\nCreating buckets..."))
        buckets = []
        for _ in range(NO_OF_BUCKETS):
            bucket = baker.make_recipe(bucket_recipe, user=user, allocation_percentage=20)
            buckets.append(bucket)
            self.stdout.write(f"Created bucket: {bucket}")
        buckets = cycle(buckets)

        # Create categories
        self.stdout.write(self.style.NOTICE("\nCreating categories..."))
        positive_categories = []
        for _ in range(NO_OF_POSITIVE_CATEGORIES):
            category = baker.make_recipe(
                positive_category_recipe,
                name=f"Positive Category {_+1}",
                sign=Category.Sign.POSITIVE,
                user=user,
            )
            positive_categories.append(category)
            self.stdout.write(f"Created positive category: {category}")
        positive_categories = cycle(positive_categories)

        negative_categories = []
        for _ in range(NO_OF_NEGATIVE_CATEGORIES):
            category = baker.make_recipe(
                negative_category_recipe,
                name=f"Negative Category {_+1}",
                sign=Category.Sign.NEGATIVE,
                user=user,
            )
            negative_categories.append(category)
            self.stdout.write(f"Created negative category: {category}")
        negative_categories = cycle(negative_categories)

        neutral_categories = []
        for _ in range(NO_OF_NEUTRAL_CATEGORIES):
            category = baker.make_recipe(
                neutral_category_recipe,
                name=f"Neutral Category {_+1}",
                sign=Category.Sign.NEUTRAL,
                user=user,
            )
            neutral_categories.append(category)
            self.stdout.write(f"Created neutral category: {category}")
        neutral_categories = cycle(neutral_categories)

        def generate_random_date():
            year = random.choice(YEARS)
            month = random.choice(MONTHS)
            day = random.randint(1, 28)
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            return make_aware(datetime(year, month, day, hour, minute))

        # Create transactions
        self.stdout.write(self.style.NOTICE("\nCreating transactions..."))

        for _ in range(NO_OF_POSITIVE_TRANSACTIONS):
            transaction_date = generate_random_date()
            transaction = baker.make_recipe(
                positive_transaction_recipe,
                location=next(locations),
                bucket=next(buckets),
                category=next(positive_categories),
                user=user,
                date=transaction_date,
            )
            self.stdout.write(f"Created positive transaction: {transaction}")

        for _ in range(NO_OF_NEGATIVE_TRANSACTIONS):
            transaction_date = generate_random_date()
            transaction = baker.make_recipe(
                negative_transaction_recipe,
                location=next(locations),
                bucket=next(buckets),
                category=next(negative_categories),
                user=user,
                date=transaction_date,
            )
            self.stdout.write(f"Created negative transaction: {transaction}")
        
        for _ in range(NO_OF_NEUTRAL_TRANSACTIONS):
            transaction_date = generate_random_date()
            transaction = baker.make_recipe(
                neutral_transaction_recipe,
                location=next(locations),
                bucket=next(buckets),
                category=next(neutral_categories),
                user=user,
                date=transaction_date,
            )
            self.stdout.write(f"Created neutral transaction: {transaction}")

        # Summary
        self.stdout.write(
            self.style.SUCCESS(f"""
Database seeding completed successfully!
Created:
- 1 user
- {NO_OF_LOCATIONS} locations
- {NO_OF_BUCKETS} buckets
- {NO_OF_POSITIVE_CATEGORIES} positive categories
- {NO_OF_NEGATIVE_CATEGORIES} negative categories
- {NO_OF_NEUTRAL_CATEGORIES} neutral categories
- {NO_OF_POSITIVE_TRANSACTIONS} positive transactions (linked to positive categories, locations and buckets)
- {NO_OF_NEGATIVE_TRANSACTIONS} negative transactions (linked to negative categories, locations and buckets)
- {NO_OF_NEUTRAL_TRANSACTIONS} neutral transactions (linked to neutral categories, locations and buckets)
- TOTAL entries created: {TOTAL_ENTRIES_CREATED}
... all linked by a single user."""))
        
        self.stdout.write(self.style.WARNING(f"""
User credentials:
Email: {USER_EMAIL}
Password: {USER_PASSWORD}
"""))
