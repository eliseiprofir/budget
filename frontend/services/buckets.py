import requests
from .auth import AuthAPIService


class BucketsAPIService(AuthAPIService):
    """API service for buckets."""

    def get_buckets(self):
        """Get all buckets for the current user."""
        self._update()
        try:
            response = requests.get(
                f"{self.base_url}/buckets/",
                headers=self.headers,
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def get_buckets_list(self):
        """Get list of buckets for the current user."""
        self._update()
        buckets_data = self.get_buckets()
        bucket_list = []
        for bucket in buckets_data:
            bucket_list.append((bucket["name"], bucket["allocation_percentage"]))
        return bucket_list
    
    def get_buckets_names(self):
        """Get names of all buckets for the current user."""
        self._update()
        buckets_data = self.get_buckets()
        buckets_names = [bucket["name"] for bucket in buckets_data]
        return buckets_names

    def get_allocation_status(self) -> bool:
        """Check if total allocation percentage exceeds 100%."""
        self._update()
        buckets_data = self.get_buckets()
        if len(buckets_data) > 0:
            allocation_status = buckets_data[0]["allocation_status"]
            return allocation_status
        return None
    
    def get_total_allocation(self) -> int:
        """Get total allocation percentage across all buckets."""
        self._update()
        buckets_data = self.get_buckets()
        total_allocation = sum([int(bucket["allocation_percentage"]) for bucket in buckets_data])
        return total_allocation

    def add_bucket(self, bucket_name: str, allocation_percentage: int):
        """Add a new bucket for the current user."""
        self._update()
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
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"

    def update_bucket(self, old_name: str, new_name: str, new_percentage: int):
        """Update a bucket's name."""
        self._update()
        bucket_id = self._get_bucket_id(old_name)
        if bucket_id is None:
            return f"Error: bucket '{old_name}' not found."
        try:
            response = requests.patch(
                f"{self.base_url}/buckets/{bucket_id}/",
                headers=self.headers,
                json={
                    "name": new_name,
                    "allocation_percentage": new_percentage,
                }
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def delete_bucket(self, bucket_name: str):
        """Delete a bucket."""
        self._update()
        bucket_id = self._get_bucket_id(bucket_name)
        if bucket_id is None:
            return f"Error: bucket '{bucket_name}' not found."
        try:
            response = requests.patch(
                f"{self.base_url}/buckets/{bucket_id}/",
                headers=self.headers,
                json={"is_removed": True}
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def _get_bucket_id(self, bucket_name: str):
        """Get ID of a bucket by its name."""
        self._update()
        buckets_data = self.get_buckets()
        for bucket in buckets_data:
            if bucket["name"] == bucket_name:
                return bucket["id"]
        return None
