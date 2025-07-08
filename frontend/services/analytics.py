import requests
from .auth import AuthAPIService


class AnalyticsAPIService(AuthAPIService):
    """API service for transactions."""

    def get_current_analytics(self):
        """Get current analytics."""
        self._update()
        try:
            response = requests.get(
                f"{self.base_url}/analytics-current/",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def get_monthly_analytics(self, year: int, month: int):
        """Get monthly analytics."""
        self._update()
        try:
            response = requests.get(
                f"{self.base_url}/analytics-monthly/{year}-{month}/",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def get_yearly_analytics(self, year: int):
        """Get yearly analytics."""
        self._update()
        try:
            response = requests.get(
                f"{self.base_url}/analytics-yearly/{year}/",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def get_historical_analytics(self):
        """Get historical analytics."""
        self._update()
        try:
            response = requests.get(
                f"{self.base_url}/analytics-historical/",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def get_years(self):
        """Get years."""
        return self._get_cached_historical_analytics()["yearly"].keys()
 