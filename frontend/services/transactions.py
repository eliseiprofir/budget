import requests
from .auth import AuthAPIService


class TransactionAPIService(AuthAPIService):
    """API service for transactions."""

    def _get_cached_transactions(self):
        """Get or fetch transaction types data."""
        if not hasattr(self, "_transactions_data") or self._transactions_data is None:
            try:
                response = requests.get(
                    f"{self.base_url}/transactions/",
                    headers=self.headers,
                )
                response.raise_for_status()
                self._transactions_data = response.json()
            except requests.exceptions.RequestException as e:
                return f"Error: {str(e)}. Response: {response.text}"
        return self._transactions_data

    def get_transactions(self):
        """Get all transactions data for the current user."""
        self._update()
        return self._get_cached_transactions()

    def get_one_transaction(self, transaction_id: str):
        """Get one transaction data."""
        self._update()
        try:
            response = requests.get(
                f"{self.base_url}/transactions/{transaction_id}/",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def _clear_cache(self):
        """Clear the cached transaction types data."""
        if hasattr(self, "_transactions_data"):
            self._transactions_data = None

    def add_transaction(
        self,
        description: str,
        category: str,
        date: str,
        amount: str,
        location: str,
        bucket: str,
        split_income: bool
    ):
        """Add a new transaction for the current user."""
        self._clear_cache()
        try:
            response = requests.post(
                f"{self.base_url}/transactions/",
                headers=self.headers,
                json={
                    "description": description,
                    "category": category,
                    "date": date,
                    "amount": amount,
                    "location": location,
                    "bucket": bucket,
                    "split_income": split_income,
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def update_transaction(
        self,
        transaction_id: str,
        description: str,
        category: str,
        date: str,
        amount: str,
        location: str,
        bucket: str,
    ):
        """Update a transaction's name."""
        transaction = self.get_one_transaction(transaction_id)
        if transaction is None:
            return f"Error: transaction '{transaction_id}' not found."
        self._clear_cache()
        try:
            response = requests.patch(
                f"{self.base_url}/transactions/{transaction_id}/",
                headers=self.headers,
                json={
                    "description": description,
                    "category": category,
                    "date": date,
                    "amount": amount,
                    "location": location,
                    "bucket": bucket,
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def delete_transaction(self, transaction_id: str):
        """Permanently delete a transaction."""
        transaction = self.get_one_transaction(transaction_id)
        if transaction is None:
            return f"Error: transaction '{transaction}' not found."
        self._clear_cache()
        try:
            response = requests.delete(
                f"{self.base_url}/transactions/{transaction_id}/",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
