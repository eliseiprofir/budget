import streamlit as st
from .locations import locations_config
from .buckets import buckets_config
from .transaction_types import transaction_types_config
from .categories import categories_config
from utils.cache_utils import fetch_and_cache_data
from utils.cache_utils import update_cache
from utils.cache_utils import clear_all_cache

def budget_config_page():
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

    locations_config()
    st.markdown("---")
    buckets_config()
    st.markdown("---")
    transaction_types_config()
    st.markdown("---")
    categories_config()
