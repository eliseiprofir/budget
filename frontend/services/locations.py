import requests
from .auth import AuthAPIService


class LocationsAPIService(AuthAPIService):
    """API service for locations."""

    def get_locations_data(self):
        """Get all locations data for the current user."""
        self._update()
        try:
            response = requests.get(
                f"{self.base_url}/locations/",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def add_location(self, location_name: str):
        """Add a new location for the current user."""
        self._update()
        try:
            response = requests.post(
                f"{self.base_url}/locations/",
                headers=self.headers,
                json={"name": location_name}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def update_location(self, id: str, new_name: str):
        """Update a location's name."""
        self._update()
        try:
            response = requests.patch(
                f"{self.base_url}/locations/{id}/",
                headers=self.headers,
                json={"name": new_name}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def delete_location(self, id: str):
        """Soft delete a location."""
        self._update()
        try:
            response = requests.patch(
                f"{self.base_url}/locations/{id}/",
                headers=self.headers,
                json={"is_removed": True}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
