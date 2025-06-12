import streamlit as st

from .locations import locations_config
from .buckets import buckets_config
from .categories import categories_config

from utils.cache_utils import fetch_and_cache_data
from utils.cache_utils import clear_all_cache
from utils.cache_utils import cache_fetched

def budget_config_page():
    """Settings page for budget application."""

    st.title("⚙️ Budget Configuration")
    st.write("Here you can configure your budget application.")
    
    if st.button("🔄 Refresh data"):
        with st.spinner("Loading data..."):
            clear_all_cache()
            fetch_and_cache_data()
        st.rerun()

    if not cache_fetched():
        fetch_and_cache_data()

    locations_config()
    buckets_config()
    categories_config()
