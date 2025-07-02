import streamlit as st


def get_or_fetch_transactions_page(page: int = 1):
    """Get or fetch transactions page."""
    if page in st.session_state["api_transactions"]["cache"]["by_page"]:
        return st.session_state["api_transactions"]["cache"]["by_page"][page]
    else:
        update_cache("transactions_by_page", page=page)
        return st.session_state["api_transactions"]["cache"]["by_page"][page]
    

def get_or_fetch_all_transactions():
    """Get or fetch all transactions."""
    if st.session_state["api_transactions"]["cache"]["by_page"] == {}:
        update_cache("all_transactions")
        return st.session_state["api_transactions"]["cache"]["all_transactions"]
    else:
        for page in range(1, st.session_state["api_transactions"]["cache"]["info"]["pages_count"] + 1):
            if page == 1:
                st.session_state["api_transactions"]["cache"]["all_transactions"] = get_or_fetch_transactions_page(page)
                continue
            else:
                transactions = get_or_fetch_transactions_page(page)
                st.session_state["api_transactions"]["cache"]["all_transactions"].extend(transactions)
        return st.session_state["api_transactions"]["cache"]["all_transactions"]


def update_cache(entity_type: str, page: int = 1):
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
        st.session_state["api_categories"]["cache"]["signs"] = st.session_state["api_categories"]["service"].get_categories_sings()

    elif entity_type == "transactions_info":
        st.session_state["api_transactions"]["cache"]["info"]["current_page"] = page
        st.session_state["api_transactions"]["cache"]["info"]["pages_count"] = st.session_state["api_transactions"]["service"].get_pages_count()
        st.session_state["api_transactions"]["cache"]["info"]["transactions_count"] = st.session_state["api_transactions"]["service"].get_transactions_count()
        st.session_state["api_transactions"]["cache"]["info"]["has_transactions"] = st.session_state["api_transactions"]["cache"]["info"]["transactions_count"] > 0

    elif entity_type == "transactions_by_page":
        st.session_state["api_transactions"]["cache"]["by_page"][page] = st.session_state["api_transactions"]["service"].get_transactions_page(page=page)["results"]
            
    elif entity_type == "all_transactions":
        st.session_state["api_transactions"]["cache"]["all_transactions"] = st.session_state["api_transactions"]["service"].get_all_transactions()

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
        st.session_state["api_transactions"]["cache"] = {
            "info": {},
            "by_page": {},
            "all_transactions": {},
        }
    
    elif entity_type == "analytics":
        st.session_state["api_analytics"]["cache"] = {}

    else:
        raise ValueError(f"Invalid entity type: {entity_type}")


def fetch_and_cache_data(all_transactions: bool = False):
    """Fetch all data and cache it in session state."""
    update_cache("locations")
    update_cache("buckets")
    update_cache("categories")
    update_cache("transactions_info")
    update_cache("transactions_by_page")
    if all_transactions:
        update_cache("all_transactions")
    update_cache("analytics")


def clear_all_cache():
    """Clear all cached data."""
    clear_cache("locations")
    clear_cache("buckets")
    clear_cache("categories")
    clear_cache("transactions")
    clear_cache("analytics")


def cache_fetched() -> bool:
    """Check if the cache has been fetched."""
    return (
        st.session_state["api_locations"]["cache"] != {}
        and st.session_state["api_buckets"]["cache"] != {}
        and st.session_state["api_categories"]["cache"] != {}
        and st.session_state["api_transactions"]["cache"] != {}
        and st.session_state["api_analytics"]["cache"] != {}
    )
