import streamlit as st

def fetch_and_cache_data():
    """Fetch all data and cache it in session state."""
    update_cache("locations")
    update_cache("buckets")
    update_cache("transaction_types")
    update_cache("categories")

def update_cache(entity_type: str):
    """Update specific entity data in cache after change."""

    if entity_type == "locations":
        st.session_state["api_locations"]["cache"]["names"] = st.session_state["api_locations"]["service"].get_locations_names()
    
    elif entity_type == "buckets":
        st.session_state["api_buckets"]["cache"]["list"] = st.session_state["api_buckets"]["service"].get_buckets_list()
        st.session_state["api_buckets"]["cache"]["names"] = st.session_state["api_buckets"]["service"].get_buckets_names()
        st.session_state["api_buckets"]["cache"]["allocation_status"] = st.session_state["api_buckets"]["service"].get_allocation_status()
        st.session_state["api_buckets"]["cache"]["total_allocation"] = st.session_state["api_buckets"]["service"].get_total_allocation()

    elif entity_type == "transaction_types":
        st.session_state["api_transaction_types"]["cache"]["list"] = st.session_state["api_transaction_types"]["service"].get_transaction_types_list()
        st.session_state["api_transaction_types"]["cache"]["names"] = st.session_state["api_transaction_types"]["service"].get_transaction_types_names()

    elif entity_type == "categories":
        st.session_state["api_categories"]["cache"]["list"] = st.session_state["api_categories"]["service"].get_categories_list()
        st.session_state["api_categories"]["cache"]["names"] = st.session_state["api_categories"]["service"].get_categories_names()

def clear_cache(entity_type: str):
    """Clear cached data for a specific entity type."""
    
    if entity_type == "locations":
        st.session_state["api_locations"]["service"]._clear_cache()
        st.session_state["api_locations"]["cache"] = {}
    
    elif entity_type == "buckets":
        st.session_state["api_buckets"]["service"]._clear_cache()
        st.session_state["api_buckets"]["cache"] = {}

    elif entity_type == "transaction_types":
        st.session_state["api_transaction_types"]["service"]._clear_cache()
        st.session_state["api_transaction_types"]["cache"] = {}
    
    elif entity_type == "categories":
        st.session_state["api_categories"]["service"]._clear_cache()
        st.session_state["api_categories"]["cache"] = {}

def clear_all_cache():
    """Clear all cached data."""
    st.session_state["api_locations"]["service"]._clear_cache()
    st.session_state["api_locations"]["cache"] = {}
    st.session_state["api_buckets"]["service"]._clear_cache()
    st.session_state["api_buckets"]["cache"] = {}
    st.session_state["api_transaction_types"]["service"]._clear_cache()
    st.session_state["api_transaction_types"]["cache"] = {}
    st.session_state["api_categories"]["service"]._clear_cache()
    st.session_state["api_categories"]["cache"] = {}
