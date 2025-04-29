import requests
from .auth import AuthAPIService


class AnalyticsAPIService(AuthAPIService):
    """API service for transactions."""

    def get_current_analytics(self):
        """Get currenty analytics."""
        try:
            response = requests.get(
                f"{self.base_url}/analytics-current/",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"

    # def _get_cached_transactions(self):
    #     """Get or fetch transaction types data."""
    #     if not hasattr(self, "_transactions_data") or self._transactions_data is None:
    #         try:
    #             response = requests.get(
    #                 f"{self.base_url}/transactions/",
    #                 headers=self.headers,
    #             )
    #             response.raise_for_status()
    #             self._transactions_data = response.json()
    #         except requests.exceptions.RequestException as e:
    #             return f"Error: {str(e)}. Response: {response.text}"
    #     return self._transactions_data

    # def get_transactions(self):
    #     """Get all transactions data for the current user."""
    #     self._update()
    #     return self._get_cached_transactions()