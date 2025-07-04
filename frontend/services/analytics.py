import requests
from .auth import AuthAPIService


class AnalyticsAPIService(AuthAPIService):
    """API service for transactions."""

    def _get_cached_current_analytics(self):
        """Get or fetch current analytics."""
        if not hasattr(self, "_current_analytics"):
            self._update()
            try:
                response = requests.get(
                    f"{self.base_url}/analytics-current/",
                    headers=self.headers,
                )
                response.raise_for_status()
                self._current_analytics = response.json()
            except requests.exceptions.RequestException as e:
                return f"Error: {str(e)}. Response: {response.text}"
        return self._current_analytics

    def get_current_analytics(self):
        """Get current analytics"""
        return self._get_cached_current_analytics()

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
            return f"Error: {str(e)}. Response: {response.text}"
    
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
            return f"Error: {str(e)}. Response: {response.text}"
    
    def _get_cached_historical_analytics(self):
        """Get or fetch historical analytics."""
        if not hasattr(self, "_historical_analytics") or self._historical_analytics is None:
            try:
                response = requests.get(
                    f"{self.base_url}/analytics-historical/",
                    headers=self.headers,
                )
                response.raise_for_status()
                self._historical_analytics = response.json()
            except requests.exceptions.RequestException as e:
                return f"Error: {str(e)}. Response: {response.text}"
        return self._historical_analytics
    
    def get_historical_analytics(self):
        """Get historical analytics."""
        return self._get_cached_historical_analytics()

    def get_years(self):
        """Get years."""
        return self._get_cached_historical_analytics()["yearly"].keys()

    def _clear_cache(self):
        """Clear cached data."""
        if hasattr(self, "_current_analytics"):
            self._current_analytics = None
        if hasattr(self, "_historical_analytics"):
            self._historical_analytics = None
