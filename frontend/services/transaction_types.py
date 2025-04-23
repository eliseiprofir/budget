import requests
import streamlit as st
from .auth import AuthAPIService


class TransactionTypesAPIService(AuthAPIService):
    """API service for transaction_types."""

    def get_transaction_types(self):
        """Get all transaction types for the current user."""
        self._update()
        try:
            response = requests.get(
                f"{self.base_url}/transaction-types/",
                headers=self.headers,
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def get_transaction_types_list(self):
        """Get list of transaction_types for the current user."""
        self._update()
        transaction_types_data = self.get_transaction_types()
        transaction_type_list = []
        for transaction_type in transaction_types_data:
            transaction_type_list.append([transaction_type["name"], transaction_type["sign"]])
        return transaction_type_list

    def get_transaction_types_names(self):
        """Get names of all transaction types for the current user."""
        self._update()
        transaction_types_data = self.get_transaction_types()
        transaction_types_names = [transaction_type["name"] for transaction_type in transaction_types_data]
        return transaction_types_names

    def add_transaction_type(self, name: str, sign: str):
        """Add a new transaction_type for the current user."""
        self._update()
        try:
            response = requests.post(
                f"{self.base_url}/transaction-types/",
                headers=self.headers,
                json={
                    "name": name,
                    "sign": sign,
                }
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def update_transaction_type_name(self, old_name: str, new_name: str):
        """Update a transaction_type's name."""
        self._update()
        
        transaction_type_id = self.get_transaction_type_id(old_name)
        if transaction_type_id is None:
            return f"Error: transaction_type '{old_name}' not found."
        
        try:
            response = requests.patch(
                f"{self.base_url}/transaction-types/{transaction_type_id}/",
                headers=self.headers,
                json={"name": new_name}
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def delete_transaction_type(self, transaction_type_name: str):
        """Delete a transaction_type."""
        self._update()

        transaction_type_id = self.get_transaction_type_id(transaction_type_name)
        if transaction_type_id is None:
            return f"Error: transaction_type '{transaction_type_name}' not found."

        try:
            response = requests.patch(
                f"{self.base_url}/transaction-types/{transaction_type_id}/",
                headers=self.headers,
                json={"is_removed": True}
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def get_transaction_type_id(self, transaction_type_name: str):
        """Get ID of a transaction_type by its name."""
        self._update()
        transaction_types_data = self.get_transaction_types()
        for transaction_type in transaction_types_data:
            if transaction_type["name"] == transaction_type_name:
                return transaction_type["id"]
        return None
    
    def get_transaction_type_name(self, transaction_type_id: str):
        """Get the name of a transaction type by its ID."""
        self._update()
        transaction_types_data = self.get_transaction_types()

        # If we receive a URL, extract the ID
        if transaction_type_id.startswith('http'):
            transaction_type_id = transaction_type_id.split("/")[-2]
        
        for transaction_type in transaction_types_data:
            if transaction_type["id"] == transaction_type_id:
                return transaction_type["name"]
        
        return None
