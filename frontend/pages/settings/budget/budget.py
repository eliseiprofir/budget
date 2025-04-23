import time
import streamlit as st
from .locations import locations_settings
from .buckets import buckets_settings
from .transaction_types import transaction_types_settings
from .categories import categories_settings

def budget_settings_page():
    """Settings page for budget application."""

    st.title("💰 Budget Configuration")
    st.write("Here you can configure your budget application.")
    locations_settings()
    st.markdown("---")
    buckets_settings()
    st.markdown("---")
    transaction_types_settings()
    st.markdown("---")
    categories_settings()
