from django.db.models import Sum
from django.db.models import DecimalField
from django.db.models.functions import Coalesce

from core.models import Location
from core.models import Bucket
from transactions.models import TransactionType
from transactions.models import Category
from transactions.models import Transaction


class AnalyticsBaseService:
    """Base service for analytics operations."""
    CACHE_TIMEOUT = 3600  # 1 hour

    def __init__(self, user):
        self.user = user
        self.locations = Location.available_objects.filter_by_user(user=self.user)
        self.buckets = Bucket.available_objects.filter_by_user(user=self.user)
        self.transaction_types = TransactionType.available_objects.filter_by_user(user=self.user)
        self.categories = Category.available_objects.filter_by_user(user=self.user)
        self.transactions = Transaction.objects.filter_by_user(user=self.user)

    def get_positive_categories(self):
        """Get all positive categories for the given user."""
        return self.categories.filter(transaction_type__sign=TransactionType.Sign.POSITIVE)

    def get_negative_categories(self):
        """Get all negative categories for the given user."""
        return self.categories.filter(transaction_type__sign=TransactionType.Sign.NEGATIVE)

    def get_neutral_categories(self):
        """Get all neutral categories for the given user."""
        return self.categories.filter(transaction_type__sign=TransactionType.Sign.NEUTRAL)

    def get_positive_transactions(self):
        """Get all positive transactions for the given user."""
        return self.transactions.filter(category__transaction_type__sign=TransactionType.Sign.POSITIVE)

    def get_negative_transactions(self):
        """Get all negative transactions for the given user."""
        return self.transactions.filter(category__transaction_type__sign=TransactionType.Sign.NEGATIVE)

    def get_neutral_transactions(self):
        """Get all neutral transactions for the given user."""
        return self.transactions.filter(category__transaction_type__sign=TransactionType.Sign.NEUTRAL)

    @staticmethod
    def sum_transactions(queryset: Transaction):
        """Sum the amount for a queryset of transactions."""
        return queryset.aggregate(
            total=Coalesce(
                Sum("amount", output_field=DecimalField()),
                0, output_field=DecimalField()
            )
        )["total"]

    def get_balance_for_queryset(self, queryset: Transaction):
        """Get balance for a specific queryset of transactions."""
        positive = self.sum_transactions(queryset.filter(
            category__transaction_type__sign=TransactionType.Sign.POSITIVE
        ))

        negative = self.sum_transactions(queryset.filter(
            category__transaction_type__sign=TransactionType.Sign.NEGATIVE
        ))

        neutral = self.sum_transactions(queryset.filter(
            category__transaction_type__sign=TransactionType.Sign.NEUTRAL
        ))

        return {
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "balance": positive - negative + neutral
        }

    def get_transactions_by_month(self, month, year):
        """Get transactions by month and year."""
        return self.transactions.filter(date__year=year, date__month=month)

    def get_transactions_by_year(self, year):
        """Get transactions by year."""
        return self.transactions.filter(date__year=year)
