import streamlit as st

def fetch_and_cache_data():
    """Fetch all data and cache it in session state."""
    update_cache("locations")
    update_cache("buckets")
    update_cache("categories")
    update_cache("transactions")
    update_cache("analytics")

def update_cache(entity_type: str):
    """Update specific entity data in cache after change."""

    if entity_type == "locations":
        st.session_state["api_locations"]["cache"]["names"] = st.session_state["api_locations"]["service"].get_locations_names()
    
    elif entity_type == "buckets":
        st.session_state["api_buckets"]["cache"]["list"] = st.session_state["api_buckets"]["service"].get_buckets_list()
        st.session_state["api_buckets"]["cache"]["names"] = st.session_state["api_buckets"]["service"].get_buckets_names()
        st.session_state["api_buckets"]["cache"]["allocation_status"] = st.session_state["api_buckets"]["service"].get_allocation_status()
        st.session_state["api_buckets"]["cache"]["total_allocation"] = st.session_state["api_buckets"]["service"].get_total_allocation()

    elif entity_type == "categories":
        st.session_state["api_categories"]["cache"]["list"] = st.session_state["api_categories"]["service"].get_categories_list()
        st.session_state["api_categories"]["cache"]["names"] = st.session_state["api_categories"]["service"].get_categories_names()
    
    elif entity_type == "transactions":
        st.session_state["api_transactions"]["cache"]["list"] = st.session_state["api_transactions"]["service"].get_transactions()
    
    elif entity_type == "analytics":
        st.session_state["api_analytics"]["cache"]["years"] = st.session_state["api_analytics"]["service"].get_years()

    else:
        raise ValueError(f"Invalid entity type: {entity_type}")

def clear_cache(entity_type: str):
    """Clear cached data for a specific entity type."""
    
    if entity_type == "locations":
        st.session_state["api_locations"]["service"]._clear_cache()
        st.session_state["api_locations"]["cache"] = {}
    
    elif entity_type == "buckets":
        st.session_state["api_buckets"]["service"]._clear_cache()
        st.session_state["api_buckets"]["cache"] = {}
    
    elif entity_type == "categories":
        st.session_state["api_categories"]["service"]._clear_cache()
        st.session_state["api_categories"]["cache"] = {}
    
    elif entity_type == "transactions":
        st.session_state["api_transactions"]["service"]._clear_cache()
        st.session_state["api_transactions"]["cache"] = {}
    
    elif entity_type == "analytics":
        st.session_state["api_analytics"]["cache"] = {}

    else:
        raise ValueError(f"Invalid entity type: {entity_type}")

def clear_all_cache():
    """Clear all cached data."""
    st.session_state["api_locations"]["service"]._clear_cache()
    st.session_state["api_locations"]["cache"] = {}
    st.session_state["api_buckets"]["service"]._clear_cache()
    st.session_state["api_buckets"]["cache"] = {}
    st.session_state["api_categories"]["service"]._clear_cache()
    st.session_state["api_categories"]["cache"] = {}
    st.session_state["api_transactions"]["service"]._clear_cache()
    st.session_state["api_transactions"]["cache"] = {}
    st.session_state["api_analytics"]["cache"] = {}
