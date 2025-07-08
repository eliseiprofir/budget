import requests
from .auth import AuthAPIService


class BucketsAPIService(AuthAPIService):
    """API service for buckets."""

    def get_buckets_data(self):
        """Get buckets data."""
        self._update()
        try:
            response = requests.get(
                f"{self.base_url}/buckets/",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def add_bucket(self, bucket_name: str, allocation_percentage: int):
        """Add a new bucket for the current user."""
        try:
            response = requests.post(
                f"{self.base_url}/buckets/",
                headers=self.headers,
                json={
                    "name": bucket_name,
                    "allocation_percentage": allocation_percentage,
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def update_bucket(self, id: str, new_name: str, new_percentage: int):
        """Update a bucket's name and percentage."""
        try:
            response = requests.patch(
                f"{self.base_url}/buckets/{id}/",
                headers=self.headers,
                json={
                    "name": new_name,
                    "allocation_percentage": new_percentage,
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def delete_bucket(self, id: str):
        """Soft delete a bucket."""
        try:
            response = requests.patch(
                f"{self.base_url}/buckets/{id}/",
                headers=self.headers,
                json={"is_removed": True}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
