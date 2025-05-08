from .base import AnalyticsBaseService


class AnalyticsHistoricalService(AnalyticsBaseService):
    """Service to provide historical analytics."""

    def __init__(self, user):
        """Initialize the historical analytics service."""
        self.user = user
        super().__init__(user)

    def get_positive_categories_by_year(self, year):
        """Get categories data for the given user."""
        categories = {}

        positive_categories = self.get_positive_categories()
        year_transactions = self.get_transactions_by_year(year=year)

        for category in positive_categories:
            year_category_transactions = year_transactions.filter(category=category)
            categories[category.name] = self.sum_transactions(year_category_transactions)

        return categories

    def get_negative_categories_by_year(self, year):
        """Get categories data for the given user."""
        categories = {}

        negative_categories = self.get_negative_categories()
        year_transactions = self.get_transactions_by_year(year=year)

        for category in negative_categories:
            year_category_transactions = year_transactions.filter(category=category)
            categories[category.name] = self.sum_transactions(year_category_transactions)

        return categories
    
    def get_neutral_categories_by_year(self, year):
        """Get categories data for the given user."""
        categories = {}

        neutral_categories = self.get_neutral_categories()
        year_transactions = self.get_transactions_by_year(year=year)

        for category in neutral_categories:
            year_category_transactions = year_transactions.filter(category=category)
            categories[category.name] = self.sum_transactions(year_category_transactions)
        
        return categories

    def get_balance_by_year(self, year):
        """Get balance for the given user."""
        year_transactions = self.get_transactions_by_year(year=year)

        return self.get_balance_for_queryset(year_transactions)

    def get_historical_data_by_year(self):
        """Get historical data by year for the given user."""

        yearly_data = {}

        years = self.transactions.dates("date", "year").distinct()

        for year_date in years:
            year = year_date.year
            data = {
                "positive_categories": self.get_positive_categories_by_year(year),
                "negative_categories": self.get_negative_categories_by_year(year),
                "neutral_categories": self.get_neutral_categories_by_year(year),
                "balance": self.get_balance_by_year(year)
            }
            yearly_data[str(year)] = data

        return yearly_data

    def get_historical_summary(self):
        """Get yearly summary for the given user."""

        historical_summary = {
            "positive_categories": {},
            "negative_categories": {},
            "neutral_categories": {},
            "balance": {}
        }

        positive_categories = self.get_positive_categories()
        negative_categories = self.get_negative_categories()
        neutral_categories = self.get_neutral_categories()

        for category in positive_categories:
            year_category_transactions = self.transactions.filter(category=category)
            historical_summary["positive_categories"][category.name] = self.sum_transactions(year_category_transactions)

        for category in negative_categories:
            year_category_transactions = self.transactions.filter(category=category)
            historical_summary["negative_categories"][category.name] = self.sum_transactions(year_category_transactions)

        for category in neutral_categories:
            year_category_transactions = self.transactions.filter(category=category)
            historical_summary["neutral_categories"][category.name] = self.sum_transactions(year_category_transactions)

        historical_summary["balance"] = self.get_balance_for_queryset(self.transactions)

        return historical_summary

    def get_summary(self):
        """Get summary of all time for the given user."""
        return {
            "yearly": self.get_historical_data_by_year(),
            "summary": self.get_historical_summary(),
        }
