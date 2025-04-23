import requests
import streamlit as st
from .auth import AuthAPIService


class CategoriesAPIService(AuthAPIService):
    """API service for categories."""

    def get_categories(self):
        """Get all categories for the current user."""
        self._update()
        try:
            response = requests.get(
                f"{self.base_url}/categories/",
                headers=self.headers,
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def get_categories_list(self):
        """Get list of categories for the current user."""
        self._update()
        transaction_types_api = st.session_state["api_transaction_types"]["service"]
        categories_data = self.get_categories()
        category_list = []
        for category in categories_data:
            transaction_type_name = transaction_types_api.get_transaction_type_name(category["transaction_type"])
            category_list.append([category["name"], transaction_type_name])
        return category_list

    def get_categories_names(self):
        """Get names of all categories for the current user."""
        self._update()
        categories_data = self.get_categories()
        categories_names = [category["name"] for category in categories_data]
        return categories_names

    def add_category(self, name: str, transaction_type_id: str):
        """Add a new category for the current user."""
        self._update()
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
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def update_category(self, old_name: str, new_name: str, new_transaction_type_id: str):
        """Update a category's name."""
        self._update()
        
        category_id = self.get_category_id(old_name)
        if category_id is None:
            return f"Error: category '{old_name}' not found."
        
        try:
            response = requests.patch(
                f"{self.base_url}/categories/{category_id}/",
                headers=self.headers,
                json={
                    "name": new_name,
                    "transaction_type": new_transaction_type_id}
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def delete_category(self, category_name: str):
        """Delete a category."""
        self._update()

        category_id = self.get_category_id(category_name)
        if category_id is None:
            return f"Error: category '{category_name}' not found."

        try:
            response = requests.patch(
                f"{self.base_url}/categories/{category_id}/",
                headers=self.headers,
                json={"is_removed": True}
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def get_category_id(self, category_name: str):
        """Get ID of a category by its name."""
        self._update()
        categories_data = self.get_categories()
        for category in categories_data:
            if category["name"] == category_name:
                return category["id"]
        return None
