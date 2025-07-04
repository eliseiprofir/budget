import requests
from .auth import AuthAPIService


class TransactionAPIService(AuthAPIService):
    """API service for transactions."""

    def get_transactions_page(self, page=1, page_size=50):
        """Get paginated transactions data."""
        self._update()
        if page == 1:
            return self._get_cached_transactions_first_page(page=page, page_size=page_size)
        else:
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
    
    def _get_cached_transactions_first_page(self, page=1, page_size=50):
        """Get first page of transactions data."""
        if not hasattr(self, "_first_page_transactions") or self._first_page_transactions is None:
            self._update()
            try:
                response = requests.get(
                    f"{self.base_url}/transactions/",
                    headers=self.headers,
                    params={"page": page, "page_size": page_size},
                )
                response.raise_for_status()
                self._first_page_transactions = response.json()
            except requests.exceptions.RequestException as e:
                return f"Error: {str(e)}. Response: {response.text}"
        return self._first_page_transactions
    
    def get_transactions_first_page(self, page=1, page_size=50):
        """Get first page of transactions data."""
        return self._get_cached_transactions_first_page(page=page, page_size=page_size)

    def _get_cached_all_transactions(self):
        """Get or fetch all transactions data."""
        if not hasattr(self, "_all_transactions") or self._all_transactions is None:
            self._update()
            all_transactions = self._get_cached_transactions_first_page()
            page = 2

            while True:
                data = self.get_transactions_page(page=page)
                if isinstance(data, str):  # Error
                    return data
                all_transactions["results"].extend(data["results"])
                if data["next"] is None:
                    break
                page += 1

            self._all_transactions = all_transactions["results"]
        
        return self._all_transactions

    def get_all_transactions(self):
        """Get all transactions by fetching all pages."""
        return self._get_cached_all_transactions()

    def get_transactions_count(self):
        """Get total number of transactions."""
        return self._get_cached_transactions_first_page()["count"]

    def get_pages_count(self, page_size: int = 50):
        """Get total number of pages."""
        return (self._get_cached_transactions_first_page()["count"] + 49) // page_size

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
        if hasattr(self, "_all_transactions"):
            self._all_transactions = None
        if hasattr(self, "_first_page_transactions"):
            self._first_page_transactions = None

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
        category_id: str,
        date: str,
        amount: str,
        location_id: str,
        bucket_id: str,
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

    def update_transaction_location(self, transaction_id: str, new_location_id: str):
        """Update a transaction's location."""
        transaction = self.get_one_transaction(transaction_id)
        category_id = transaction["category"]["id"]
        bucket_id = transaction["bucket"]["id"]
        if transaction is None:
            return f"Error: transaction '{transaction_id}' not found."
        self._clear_cache()
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
        transaction = self.get_one_transaction(transaction_id)
        category_id = transaction["category"]["id"]
        location_id = transaction["location"]["id"]
        if transaction is None:
            return f"Error: transaction '{transaction_id}' not found."
        self._clear_cache()
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
        transaction = self.get_one_transaction(transaction_id)
        location_id = transaction["location"]["id"]
        bucket_id = transaction["bucket"]["id"]
        if transaction is None:
            return f"Error: transaction '{transaction_id}' not found."
        self._clear_cache()
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
