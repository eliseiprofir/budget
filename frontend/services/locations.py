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
            return f"Error: {str(e)}. Response: {response.text}"

    def get_locations_list(self):
        """Get list of locations for the current user."""
        self._update()
        locations_data = self.get_locations()
        location_list = []
        for location in locations_data:
            location_list.append(location["name"])
        return location_list

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
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def update_location(self, old_name: str, new_name: str):
        """Update a location's name."""
        self._update()
        
        location_id = self._get_location_id(old_name)
        if location_id is None:
            return f"Error: Location '{old_name}' not found."
        
        try:
            response = requests.patch(
                f"{self.base_url}/locations/{location_id}/",
                headers=self.headers,
                json={"name": new_name}
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def delete_location(self, location_name: str):
        """Delete a location."""
        self._update()

        location_id = self._get_location_id(location_name)
        if location_id is None:
            return f"Error: Location '{location_name}' not found."

        try:
            response = requests.patch(
                f"{self.base_url}/locations/{location_id}/",
                headers=self.headers,
                json={"is_removed": True}
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def _get_location_id(self, location_name: str):
        """Get ID of a location by its name."""
        self._update()
        locations_data = self.get_locations()
        for location in locations_data:
            if location["name"] == location_name:
                return location["id"]
        return None