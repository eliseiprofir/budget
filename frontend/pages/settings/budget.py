import streamlit as st

def budget_settings_page():
    """Settings page for budget application."""

    st.title("💰 Budget Configuration")

    st.header("Locations")
    st.write("Configure your locations here. You can add, edit or delete your locations.")

    location_api = st.session_state["api_locations"]["service"]
    locations = location_api.get_locations()
    st.write(locations)
