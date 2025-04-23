import requests
from .auth import AuthAPIService


class BucketsAPIService(AuthAPIService):
    """API service for buckets."""

    def _get_cached_buckets(self):
        """Get or fetch buckets data."""
        if not hasattr(self, "_buckets_data") or self._buckets_data is None:
            try:
                response = requests.get(
                    f"{self.base_url}/buckets/",
                    headers=self.headers,
                )
                response.raise_for_status()
                self._buckets_data = response.json()
            except requests.exceptions.RequestException as e:
                return f"Error: {str(e)}. Response: {response.text}"
        return self._buckets_data

    def get_buckets(self):
        """Get all buckets data for the current user."""
        self._update()
        return self._get_cached_buckets()

    def get_buckets_list(self):
        """Get list of buckets and their allocations."""
        buckets_data = self.get_buckets()
        return [(bucket["name"], bucket["allocation_percentage"]) for bucket in buckets_data]

    def get_buckets_names(self):
        """Get names of all buckets."""
        buckets_data = self.get_buckets()
        return [bucket["name"] for bucket in buckets_data]

    def get_total_allocation(self) -> int:
        """Get total allocation percentage."""
        buckets_data = self.get_buckets()
        return sum(int(bucket["allocation_percentage"]) for bucket in buckets_data)

    def get_allocation_status(self) -> bool:
        """Check if total allocation percentage is 100%."""
        return "COMPLETE" if self.get_total_allocation() == 100 else "INCOMPLETE"

    def get_bucket_id(self, bucket_name: str):
        """Get ID of a bucket by its name."""
        buckets_data = self.get_buckets()
        for bucket in buckets_data:
            if bucket["name"] == bucket_name:
                return bucket["id"]
        return None

    def _clear_cache(self):
        """Clear the cached buckets data."""
        if hasattr(self, "_buckets_data"):
            self._buckets_data = None
    
    def add_bucket(self, bucket_name: str, allocation_percentage: int):
        """Add a new bucket for the current user."""
        self._clear_cache()
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

    def update_bucket(self, old_name: str, new_name: str, new_percentage: int):
        """Update a bucket's name and percentage."""
        bucket_id = self.get_bucket_id(old_name)
        if bucket_id is None:
            return f"Error: bucket '{old_name}' not found."
        self._clear_cache()
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
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
    
    def delete_bucket(self, bucket_name: str):
        """Soft delete a bucket."""
        bucket_id = self.get_bucket_id(bucket_name)
        if bucket_id is None:
            return f"Error: bucket '{bucket_name}' not found."
        self._clear_cache()
        try:
            response = requests.patch(
                f"{self.base_url}/buckets/{bucket_id}/",
                headers=self.headers,
                json={"is_removed": True}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}. Response: {response.text}"
