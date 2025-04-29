import requests
import streamlit as st
from .auth import AuthAPIService


class CategoriesAPIService(AuthAPIService):
    """API service for categories."""

    def _get_cached_categories(self):
        """Get or fetch categories data."""
        if not hasattr(self, "_categories_data") or self._categories_data is None:
            try:
                response = requests.get(
                    f"{self.base_url}/categories/",
                    headers=self.headers,
                )
                response.raise_for_status()
                self._categories_data = response.json()
            except requests.exceptions.RequestException as e:
                return f"Error: {str(e)}. Response: {response.text}"
        return self._categories_data

    def get_categories(self):
        """Get all categories data for the current user."""
        self._update()
        return self._get_cached_categories()

    def get_categories_list(self):
        """Get list of categories and their transaction types."""
        categories_data = self.get_categories()
        category_list = []
        for category in categories_data:
            category_list.append([category["name"], category["transaction_type"]["name"]])
        return category_list

    def get_categories_names(self):
        """Get names of all categories."""
        categories_data = self.get_categories()
        return [category["name"] for category in categories_data]

    def get_category_id(self, category_name: str):
        """Get ID of a category by its name."""
        categories_data = self.get_categories()
        for category in categories_data:
            if category["name"] == category_name:
                return category["id"]
        return None

    def get_category_type_sign(self, category_id: str):
        """Get transaction type of a category by its ID."""
        categories_data = self.get_categories()
        for category in categories_data:
            if category["id"] == category_id:
                return category["transaction_type"]["sign"]
        return None

    def _clear_cache(self):
        """Clear the cached categories data."""
        if hasattr(self, "_categories_data"):
            self._categories_data = None

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

    def add_category(self, name: str, transaction_type_id: str):
        """Add a new category for the current user."""
        self._clear_cache()
        try:
            response = requests.post(
                f"{self.base_url}/categories/",
                headers=self.headers,
                json={
                    "name": name,
                    "transaction_type": transaction_type_id,
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def update_category(self, old_name: str, new_name: str, new_transaction_type_id: str):
        """Update a category's name and transaction type."""
        category_id = self.get_category_id(old_name)
        if category_id is None:
            return f"Error: category '{old_name}' not found."
        self._clear_cache()
        try:
            response = requests.patch(
                f"{self.base_url}/categories/{category_id}/",
                headers=self.headers,
                json={
                    "name": new_name,
                    "transaction_type": new_transaction_type_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def delete_category(self, category_name: str):
        """Soft delete a category."""
        category_id = self.get_category_id(category_name)
        if category_id is None:
            return f"Error: category '{category_name}' not found."
        self._clear_cache()
        try:
            response = requests.patch(
                f"{self.base_url}/categories/{category_id}/",
                headers=self.headers,
                json={"is_removed": True}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
