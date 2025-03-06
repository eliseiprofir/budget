from .base import AnalyticsBaseService


class AnalyticsMonthlyService(AnalyticsBaseService):
    """Service to provide monthly analytics."""

    def __init__(self, user, year, month):
        """Initialize the monthly analytics service."""
        self.user = user
        self.year = year
        self.month = month
        super().__init__(user)

    def get_positive_categories_data(self):
        """Get positive categories data for specific month for the given user."""
        categories = {}

        positive_categories = self.get_positive_categories()
        month_transactions = self.get_transactions_by_month(
            year=self.year,
            month=self.month
        )

        for category in positive_categories:
            month_category_transactions = month_transactions.filter(category=category)
            categories[category.name] = self.sum_transactions(month_category_transactions)

        return categories

    def get_negative_categories_data(self):
        """Get negative categories data for specific month for the given user."""
        categories = {}

        negative_categories = self.get_negative_categories()
        month_transactions = self.get_transactions_by_month(
            year=self.year,
            month=self.month
        )

        for category in negative_categories:
            month_category_transactions = month_transactions.filter(category=category)
            categories[category.name] = self.sum_transactions(month_category_transactions)

        return categories


    def get_balance(self):
        """Get balance for specific month for the given user."""
        month_transactions = self.get_transactions_by_month(
                year=self.year,
                month=self.month
            )

        return self.get_balance_for_queryset(month_transactions)
