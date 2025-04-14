import requests
import streamlit as st

class AuthAPIService:
    def __init__(self):
        self.base_url = "http://backend:8000/api"
        self.headers = {
            "Content-Type": "application/json"
        }
        self.token = st.session_state.get("token")
        self.user_id = st.session_state.get("user_id")

    def _update_user_id(self, user_id):
        """Helper function to update the user ID."""
        self.user_id = user_id
        st.session_state["user_id"] = user_id

    def login(self, email: str, password: str) -> dict:
        """Authenticate user and get JWT token"""
        try:
            response = requests.post(
                f"{self.base_url}/token/",
                json={
                    "email": email,
                    "password": password
                },
                timeout=10 
            )
            response.raise_for_status()
            data = response.json()
            if "access" in data:
                self.token = data["access"]
                st.session_state["token"] = self.token
                self.headers["Authorization"] = f"Bearer {self.token}"
            return data
        except requests.exceptions.RequestException as e:
            return f"Connection error: {str(e)}"

    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.token is not None

    def logout(self):
        """Clear authentication token"""
        self.token = None
        if "Authorization" in self.headers:
            del self.headers["Authorization"]

    def get_user_info(self):
        """Get user information"""
        if not self.is_authenticated():
            return None
            
        try:
            response = requests.get(
                f"{self.base_url}/users/",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            user_data = response.json()[0]
            self._update_user_id(user_data["id"])
            return user_data
        except requests.exceptions.RequestException as e:
            print(f"Error getting user info: {str(e)}")
            return None

    def update_user(self, name: str, email: str, password: str = None):
        """Update user information"""
        if not self.is_authenticated():
            return "Not authenticated."

        update_data = {
            "full_name": name,
            "email": email,
        }
        
        if password and password.strip():
            update_data["password"] = password

        try:
            response = requests.put(
                f"{self.base_url}/users/{self.user_id}/",
                json=update_data,
                headers=self.headers,
                timeout=10
            )            
            if response.status_code == 200:
                return response.json()
            else:
                return f"Error: {response.text}"
            
        except requests.exceptions.RequestException as e:
            return f"Connection error: {str(e)}"

    def signup(self, name: str, email: str, password: str):
        """Register a new user"""

        try:
            response = requests.post(
                f"{self.base_url}/users/",
                json={
                    "email": email,
                    "full_name": name,
                    "password": password,
                },
                headers={"Content-Type": "application/json"},
                timeout=10
            )            
            if response.status_code == 201:
                return response.json()
            else:
                return f"Error: {response.text}"
            
        except requests.exceptions.RequestException as e:
            return f"Connection error: {str(e)}"
