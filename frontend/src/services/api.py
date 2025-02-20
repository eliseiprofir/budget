import requests

class APIService:
    def __init__(self):
        self.base_url = "http://localhost:8000/api"
        self.headers = {
            "Content-Type": "application/json"
        }
        self.token = None

    def login(self, username: str, password: str) -> dict:
        """
        Authenticate user and get JWT token
        """
        try:
            response = requests.post(
                f"{self.base_url}/token/",
                json={
                    "username": username,
                    "password": password
                }
            )
            response.raise_for_status()  # Raise exception for 4XX/5XX status codes
            data = response.json()
            if "access" in data:
                self.token = data["access"]
                self.headers["Authorization"] = f"Bearer {self.token}"
            return data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Login failed: {str(e)}")

    def is_authenticated(self) -> bool:
        """
        Check if user is authenticated
        """
        return self.token is not None

    def logout(self):
        """
        Clear authentication token
        """
        self.token = None
        if "Authorization" in self.headers:
            del self.headers["Authorization"]
