from transactions.models import TransactionType
from transactions.models import Transaction

from .base import AnalyticsBaseService


class AnalyticsCurrentService(AnalyticsBaseService):
    """Service to provide current status analytics."""

    def get_locations_data(self):
        """Get locations data for the given user."""
        locations = {"total": 0}

        for location in self.locations:
            location_transactions = self.transactions.filter(location=location)
            location_balance = self.get_balance_for_queryset(location_transactions)
            locations[location.name] = location_balance["balance"]
            locations["total"] += locations[location.name]

        return locations

    def get_buckets_data(self):
        """Get buckets data for the given user."""
        buckets = {"total": 0}

        for bucket in self.buckets:
            bucket_transactions = self.transactions.filter(bucket=bucket)
            bucket_balance = self.get_balance_for_queryset(bucket_transactions)
            buckets[bucket.name] = bucket_balance["balance"]
            buckets["total"] += buckets[bucket.name]

        return buckets

    def get_balance(self):
        """Get balance for the given user."""
        return self.get_balance_for_queryset(self.transactions)

    def get_summary(self):
        """Get complete summary of current status for the given user."""
        return {
            "locations": self.get_locations_data(),
            "buckets": self.get_buckets_data(),
            "balance": self.get_balance(),
        }
