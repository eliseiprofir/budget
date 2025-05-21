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

    def get_monthly_analytics(self, year: int, month: int):
        """Get monthly analytics."""
        try:
            response = requests.get(
                f"{self.base_url}/analytics-monthly/{year}-{month}/",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
    
    def get_yearly_analytics(self, year: int):
        """Get yearly analytics."""
        try:
            response = requests.get(
                f"{self.base_url}/analytics-yearly/{year}/",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
    
    def get_years(self):
        """Get years."""
        try:
            response = requests.get(
                f"{self.base_url}/analytics-historical/",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()["yearly"].keys()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
