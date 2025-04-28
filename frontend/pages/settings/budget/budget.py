import time
import streamlit as st
from .locations import locations_settings
from .buckets import buckets_settings
from .transaction_types import transaction_types_settings
from .categories import categories_settings
from utils.cache_utils import fetch_and_cache_data
from utils.cache_utils import update_cache
from utils.cache_utils import clear_all_cache

def budget_settings_page():
    """Settings page for budget application."""

    st.title("💰 Budget Configuration")
    st.write("Here you can configure your budget application.")
    
    if st.button("🔄 Refresh data"):
        clear_all_cache()
        fetch_and_cache_data()
        st.rerun()

    if st.session_state["api_locations"]["cache"] == {}:
        update_cache("locations")
    if st.session_state["api_buckets"]["cache"] == {}:
        update_cache("buckets")
    if st.session_state["api_transaction_types"]["cache"] == {}:
        update_cache("transaction_types")
    if st.session_state["api_categories"]["cache"] == {}:
        update_cache("categories")

    locations_settings()
    st.markdown("---")
    buckets_settings()
    st.markdown("---")
    transaction_types_settings()
    st.markdown("---")
    categories_settings()
