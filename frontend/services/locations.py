import requests
from .auth import AuthAPIService


class LocationsAPIService(AuthAPIService):
    """API service for locations."""

    def _get_cached_locations(self):
        """Get or fetch locations data."""
        if not hasattr(self, "_locations_data") or self._locations_data is None:
            try:
                response = requests.get(
                    f"{self.base_url}/locations/",
                    headers=self.headers,
                )
                response.raise_for_status()
                self._locations_data = response.json()
            except requests.exceptions.RequestException as e:
                return f"Error: {str(e)}. Response: {response.text}"
        return self._locations_data

    def get_locations(self):
        """Get all locations data for the current user."""
        self._update()
        return self._get_cached_locations()

    def get_locations_names(self):
        """Get names of all locations."""
        locations_data = self.get_locations()
        return [location["name"] for location in locations_data]

    def get_location_id(self, location_name: str):
        """Get ID of a location by its name."""
        locations_data = self.get_locations()
        for location in locations_data:
            if location["name"] == location_name:
                return location["id"]
        return None

    def _clear_cache(self):
        """Clear the cached locations data."""
        if hasattr(self, "_locations_data"):
            self._locations_data = None

    def add_location(self, location_name: str):
        """Add a new location for the current user."""
        self._clear_cache()
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

    def update_location(self, old_name: str, new_name: str):
        """Update a location's name."""
        location_id = self.get_location_id(old_name)
        if location_id is None:
            return f"Error: Location '{old_name}' not found."
        self._clear_cache()
        try:
            response = requests.patch(
                f"{self.base_url}/locations/{location_id}/",
                headers=self.headers,
                json={"name": new_name}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def delete_location(self, location_name: str):
        """Soft delete a location."""
        location_id = self.get_location_id(location_name)
        if location_id is None:
            return f"Error: Location '{location_name}' not found."
        self._clear_cache()
        try:
            response = requests.patch(
                f"{self.base_url}/locations/{location_id}/",
                headers=self.headers,
                json={"is_removed": True}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
