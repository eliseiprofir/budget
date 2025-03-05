from django.utils import timezone

from transactions.models import TransactionType
from transactions.models import Transaction

from .base import AnalyticsBaseService
from .monthly import AnalyticsMonthlyService


class AnalyticsYearlyService(AnalyticsBaseService):
    """Service to provide yearly analytics."""

    def __init__(self, user, year):
        """Initialize the yearly analytics service."""
        self.user = user
        self.year = year
        super().__init__(user)

    def get_positive_categories_data_by_month(self, month):
        """Get categories data for the given user."""
        categories = {}

        positive_categories = self.get_positive_categories()
        month_transactions = self.get_transactions_by_month(month=month, year=self.year)

        for category in positive_categories:
            month_category_transactions = month_transactions.filter(category=category)
            categories[category.name] = self.sum_transactions(month_category_transactions)

        return categories

    def get_negative_categories_data_by_month(self, month):
        """Get categories data for the given user."""
        categories = {}

        negative_categories = self.get_negative_categories()
        month_transactions = self.get_transactions_by_month(month=month, year=self.year)

        for category in negative_categories:
            month_category_transactions = month_transactions.filter(category=category)
            categories[category.name] = self.sum_transactions(month_category_transactions)

        return categories


    def get_balance_by_month(self, month):
        """Get balance for the given user."""
        month_transactions = self.get_transactions_by_month(month=month, year=self.year)

        return self.get_balance_for_queryset(month_transactions)

    def get_year_data_by_month(self):
        """Get year data by month for the given user."""

        monthly_data = {}

        for month in range(1, 13):
            data = {
                "positive_categories": self.get_positive_categories_data_by_month(month),
                "negative_categories": self.get_negative_categories_data_by_month(month),
                "balance": self.get_balance_by_month(month)
            }
            monthly_data[str(month)] = data

        return monthly_data

    def get_year_summary(self):
        """Get yearly summary for the given user."""

        year_summary = {
            "positive_categories": {},
            "negative_categories": {},
            "balance": {}
        }

        positive_categories = self.get_positive_categories()
        negative_categories = self.get_negative_categories()
        year_transactions = self.get_transactions_by_year(year=self.year)

        for category in positive_categories:
            year_category_transactions = year_transactions.filter(category=category)
            year_summary["positive_categories"][category.name] = self.sum_transactions(year_category_transactions)

        for category in negative_categories:
            year_category_transactions = year_transactions.filter(category=category)
            year_summary["negative_categories"][category.name] = self.sum_transactions(year_category_transactions)

        year_summary["balance"] = self.get_balance_for_queryset(year_transactions)

        return year_summary
