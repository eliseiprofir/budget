import requests
from .auth import AuthAPIService


class TransactionTypesAPIService(AuthAPIService):
    """API service for transaction_types."""

    def _get_cached_transaction_types(self):
        """Get or fetch transaction types data."""
        if not hasattr(self, "_transaction_types_data") or self._transaction_types_data is None:
            try:
                response = requests.get(
                    f"{self.base_url}/transaction-types/",
                    headers=self.headers,
                )
                response.raise_for_status()
                self._transaction_types_data = response.json()
            except requests.exceptions.RequestException as e:
                return f"Error: {str(e)}. Response: {response.text}"
        return self._transaction_types_data

    def get_transaction_types(self):
        """Get all transaction_types data for the current user."""
        self._update()
        return self._get_cached_transaction_types()

    def get_transaction_types_list(self):
        """Get list of transaction_types and their signs."""
        transaction_types_data = self.get_transaction_types()
        return [(transaction_type["name"], transaction_type["sign"]) for transaction_type in transaction_types_data]

    def get_transaction_types_names(self):
        """Get names of all transaction types."""
        transaction_types_data = self.get_transaction_types()
        return [transaction_type["name"] for transaction_type in transaction_types_data]

    def get_transaction_type_id(self, transaction_type_name: str):
        """Get ID of a transaction_type by its name."""
        transaction_types_data = self.get_transaction_types()
        for transaction_type in transaction_types_data:
            if transaction_type["name"] == transaction_type_name:
                return transaction_type["id"]
        return None
    
    def get_transaction_type_name(self, transaction_type_id: str):
        """Get the name of a transaction type by its ID."""
        transaction_types_data = self.get_transaction_types()
        for transaction_type in transaction_types_data:
            if transaction_type["id"] == transaction_type_id:
                return transaction_type["name"]
        return None

    def _clear_cache(self):
        """Clear the cached transaction types data."""
        if hasattr(self, "_transaction_types_data"):
            self._transaction_types_data = None

    def add_transaction_type(self, name: str, sign: str):
        """Add a new transaction_type for the current user."""
        self._clear_cache()
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
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def update_transaction_type_name(self, old_name: str, new_name: str):
        """Update a transaction_type's name."""
        transaction_type_id = self.get_transaction_type_id(old_name)
        if transaction_type_id is None:
            return f"Error: transaction_type '{old_name}' not found."
        self._clear_cache()
        try:
            response = requests.patch(
                f"{self.base_url}/transaction-types/{transaction_type_id}/",
                headers=self.headers,
                json={"name": new_name}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def delete_transaction_type(self, transaction_type_name: str):
        """Soft delete a transaction_type."""
        transaction_type_id = self.get_transaction_type_id(transaction_type_name)
        if transaction_type_id is None:
            return f"Error: transaction_type '{transaction_type_name}' not found."
        self._clear_cache()
        try:
            response = requests.patch(
                f"{self.base_url}/transaction-types/{transaction_type_id}/",
                headers=self.headers,
                json={"is_removed": True}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
