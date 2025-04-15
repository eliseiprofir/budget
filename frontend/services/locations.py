import requests
import streamlit as st
from .auth import AuthAPIService


class LocationsAPIService(AuthAPIService):
    """API service for locations."""

    def get_locations(self):
        """Get all locations for the current user."""
        self._update()
        try:
            response = requests.get(
                f"{self.base_url}/locations/",
                headers=self.headers,
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Connection error: {str(e)}"
