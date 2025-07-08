import streamlit as st

from .locations import locations_config
from .buckets import buckets_config
from .categories import categories_config

from utils.cache_utils import update_cache
from utils.cache_utils import cache_fetched

from utils.cache_utils import get_or_fetch_locations_data
from utils.cache_utils import get_or_fetch_buckets_data
from utils.cache_utils import get_or_fetch_categories_data
from utils.cache_utils import get_or_fetch_transactions_page

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
                "transactions"
            ])
        st.rerun()
    
    if not cache_fetched(["locations", "buckets", "categories", "transactions"]):
        with st.spinner("Loading data..."):
            get_or_fetch_locations_data()
            get_or_fetch_buckets_data()
            get_or_fetch_categories_data()
            get_or_fetch_transactions_page()

    locations_config()
    buckets_config()
    categories_config()
