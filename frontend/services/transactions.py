import requests
from .auth import AuthAPIService


class TransactionAPIService(AuthAPIService):
    """API service for transactions."""

    def get_transactions_by_page(self, page=1, page_size=50):
        """Get a page of transactions data."""
        self._update()
        try:
            response = requests.get(
                f"{self.base_url}/transactions/",
                headers=self.headers,
                params={"page": page, "page_size": page_size},
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
        
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
        self._update()
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
        category_id: str,
        date: str,
        amount: str,
        location_id: str,
        bucket_id: str,
    ):
        """Update a transaction's name."""
        self._update()
        transaction = self.get_one_transaction(transaction_id)
        if transaction is None:
            return f"Error: transaction '{transaction_id}' not found."
        try:
            response = requests.patch(
                f"{self.base_url}/transactions/{transaction_id}/",
                headers=self.headers,
                json={
                    "description": description,
                    "category": category_id,
                    "date": date,
                    "amount": amount,
                    "location": location_id,
                    "bucket": bucket_id,
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def delete_transaction(self, transaction_id: str):
        """Permanently delete a transaction."""
        self._update()
        transaction = self.get_one_transaction(transaction_id)
        if transaction is None:
            return f"Error: transaction '{transaction}' not found."
        try:
            response = requests.delete(
                f"{self.base_url}/transactions/{transaction_id}/",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def update_transaction_location(self, transaction_id: str, new_location_id: str):
        """Update a transaction's location."""
        self._update()
        transaction = self.get_one_transaction(transaction_id)
        category_id = transaction["category"]["id"]
        bucket_id = transaction["bucket"]["id"]
        if transaction is None:
            return f"Error: transaction '{transaction_id}' not found."
        try:
            response = requests.patch(
                f"{self.base_url}/transactions/{transaction_id}/",
                headers=self.headers,
                json={
                    "description": transaction["description"],
                    "category": category_id,
                    "date": transaction["date"],
                    "amount": transaction["amount"],
                    "location": new_location_id,
                    "bucket": bucket_id,
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def update_transaction_bucket(self, transaction_id: str, new_bucket_id: str):
        """Update a transaction's bucket."""
        self._update()
        transaction = self.get_one_transaction(transaction_id)
        category_id = transaction["category"]["id"]
        location_id = transaction["location"]["id"]
        if transaction is None:
            return f"Error: transaction '{transaction_id}' not found."
        try:
            response = requests.patch(
                f"{self.base_url}/transactions/{transaction_id}/",
                headers=self.headers,
                json={
                    "description": transaction["description"],
                    "category": category_id,
                    "date": transaction["date"],
                    "amount": transaction["amount"],
                    "location": location_id,
                    "bucket": new_bucket_id,
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def update_transaction_category(self, transaction_id: str, new_category_id: str):
        """Update a transaction's category."""
        self._update()
        transaction = self.get_one_transaction(transaction_id)
        location_id = transaction["location"]["id"]
        bucket_id = transaction["bucket"]["id"]
        if transaction is None:
            return f"Error: transaction '{transaction_id}' not found."
        try:
            response = requests.patch(
                f"{self.base_url}/transactions/{transaction_id}/",
                headers=self.headers,
                json={
                    "description": transaction["description"],
                    "category": new_category_id,
                    "date": transaction["date"],
                    "amount": transaction["amount"],
                    "location": location_id,
                    "bucket": bucket_id,
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
