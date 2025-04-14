import streamlit as st

def settings_account_page():
    """Settings page for user's account."""

    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.error("You need to be logged in to access this page")
        st.stop()

    with st.form("edit_profile"):
        st.subheader("👤 Edit your account")
        
        api = st.session_state.get('auth_api')
        user_info = api.get_user_info() or {}

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
