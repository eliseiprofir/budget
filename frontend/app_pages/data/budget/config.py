import streamlit as st

from .locations import locations_config
from .buckets import buckets_config
from .categories import categories_config

from utils.cache_utils import update_cache

def budget_config_page():
    """Settings page for budget application."""

    st.title("⚙️ Budget Configuration")
    st.write("Here you can configure your budget application.")
    
    if st.button("🔄 Refresh data"):
        with st.spinner("Loading data..."):
            update_cache([
                "locations",
                "buckets",
                "categories",
                "transactions_info"
            ])
        st.rerun()

    locations_config()
    buckets_config()
    categories_config()
