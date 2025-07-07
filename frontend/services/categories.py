import requests
import streamlit as st
from .auth import AuthAPIService


class CategoriesAPIService(AuthAPIService):
    """API service for categories."""

    def get_categories(self):
        """Get categories data."""
        try:
            response = requests.get(
                f"{self.base_url}/categories/",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def get_category(self, id: str):
        """Get details of a category."""
        self._update()
        try:
            response = requests.get(
                f"{self.base_url}/categories/{id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def add_category(self, name: str, sign: str):
        """Add a new category for the current user."""
        try:
            response = requests.post(
                f"{self.base_url}/categories/",
                headers=self.headers,
                json={
                    "name": name,
                    "sign": sign,
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def update_category(self, id: str, new_name: str, new_sign: str):
        """Update a category's name and transaction type."""
        try:
            response = requests.patch(
                f"{self.base_url}/categories/{id}/",
                headers=self.headers,
                json={
                    "name": new_name,
                    "sign": new_sign}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def delete_category(self, id: str):
        """Soft delete a category."""
        try:
            response = requests.patch(
                f"{self.base_url}/categories/{id}/",
                headers=self.headers,
                json={"is_removed": True}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
