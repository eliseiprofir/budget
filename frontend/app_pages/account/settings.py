import streamlit as st

from utils.cache_utils import clear_cache
from utils.cache_utils import get_or_fetch_user_info


def account_settings_page():
    """Settings page for user's account."""

    if not st.session_state["api_auth"]["authenticated"]:
        st.error("You need to be logged in to access this page")
        st.stop()
    
    with st.form("edit_profile"):
        st.subheader("👤 Edit your account")
        
        api = st.session_state["api_auth"]["service"]
        user_info = get_or_fetch_user_info()
        name = st.text_input("Name *", value=user_info.get("full_name", "")).strip()
        email = st.text_input("Email *", value=user_info.get("email", "")).strip()

        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("New Password", type="password")
        with col2:
            confirm_password = st.text_input("Confirm Password", type="password")

        submitted = st.form_submit_button("Save Changes")
        if submitted:
            if not (name and email):
                st.error("Name and email fields are required.")
            elif password and password != confirm_password:
                st.error("Passwords do not match.")
            else:
                response = api.update_user(name=name, email=email, password=password)
                if isinstance(response, dict):
                    st.success("Profile updated successfully")
                    if password:
                        st.warning("Please remember the new password next time when you login")
                elif "email already exists" in response:
                    st.error("Email already exists. Please use a different email.")
                else:
                    st.error(f"Failed to update profile: {response}")
            clear_cache(["user_info"])

    st.info("If you want to delete your account, please contact us at contact@elisei.pro. We will remove all of your data within 7 days after receiving your request. Thank you!")
