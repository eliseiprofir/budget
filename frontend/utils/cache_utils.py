import streamlit as st
import datetime

current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month

# USER CACHE UTILS
def get_or_fetch_user_info():
    """Get or fetch user info."""
    if st.session_state["api_auth"]["cache"] == {}:
        update_cache(["user_info"])
        return st.session_state["api_auth"]["cache"]["user_info"]
    else:
        return st.session_state["api_auth"]["cache"]["user_info"]


# LOCATIONS CACHE UTILS
def get_or_fetch_locations_data():
    """Get or fetch locations names."""
    if st.session_state["api_locations"]["cache"] == {}:
        update_cache(["locations"])
        return st.session_state["api_locations"]["cache"]["data"]
    else:
        return st.session_state["api_locations"]["cache"]["data"]

def get_or_fetch_locations_names():
    """Get or fetch locations names."""
    if st.session_state["api_locations"]["cache"] == {}:
        update_cache(["locations"])
        return st.session_state["api_locations"]["cache"]["names"]
    else:
        return st.session_state["api_locations"]["cache"]["names"]

def get_location_id(name: str):
    """Get category id by name."""
    locations = get_or_fetch_locations_data()
    for location in locations:
        if location["name"] == name:
            return location["id"]
    return None


# BUCKETS CACHE UTILS
def get_or_fetch_buckets_data():
    """Get or fetch buckets data."""
    if st.session_state["api_buckets"]["cache"] == {}:
        update_cache(["buckets"])
        return st.session_state["api_buckets"]["cache"]["data"]
    else:
        return st.session_state["api_buckets"]["cache"]["data"]

def get_or_fetch_buckets_names():
    """Get or fetch buckets names."""
    if st.session_state["api_buckets"]["cache"] == {}:
        update_cache(["buckets"])
        return st.session_state["api_buckets"]["cache"]["names"]
    else:
        return st.session_state["api_buckets"]["cache"]["names"]

def get_or_fetch_buckets_names_allocations():
    """Get or fetch buckets names and allocations."""
    if st.session_state["api_buckets"]["cache"] == {}:
        update_cache(["buckets"])
        return st.session_state["api_buckets"]["cache"]["names_allocations"]
    else:
        return st.session_state["api_buckets"]["cache"]["names_allocations"]

def get_or_fetch_buckets_total_allocation():
    """Get or fetch buckets total_allocation."""
    if st.session_state["api_buckets"]["cache"] == {}:
        update_cache(["buckets"])
        return st.session_state["api_buckets"]["cache"]["total_allocation"]
    else:
        return st.session_state["api_buckets"]["cache"]["total_allocation"]

def get_or_fetch_buckets_allocation_status():
    """Get or fetch buckets allocation status."""
    if st.session_state["api_buckets"]["cache"] == {}:
        update_cache(["buckets"])
        return st.session_state["api_buckets"]["cache"]["allocation_status"]
    else:
        return st.session_state["api_buckets"]["cache"]["allocation_status"]

def get_bucket_id(name: str):
    """Get bucket id by name."""
    buckets = get_or_fetch_buckets_data()
    for bucket in buckets:
        if bucket["name"] == name:
            return bucket["id"]
    return None


# CATEGORIES CACHE UTILS
def get_or_fetch_categories_data():
    """Get or fetch categories data."""
    if st.session_state["api_categories"]["cache"] == {}:
        update_cache(["categories"])
        return st.session_state["api_categories"]["cache"]["data"]
    else:
        return st.session_state["api_categories"]["cache"]["data"]

def get_or_fetch_categories_names():
    """Get or fetch categories names."""
    if st.session_state["api_categories"]["cache"] == {}:
        update_cache(["categories"])
        return st.session_state["api_categories"]["cache"]["names"]
    else:
        return st.session_state["api_categories"]["cache"]["names"]

def get_or_fetch_categories_names_signs():
    """Get or fetch categories names and signs."""
    if st.session_state["api_categories"]["cache"] == {}:
        update_cache(["categories"])
        return st.session_state["api_categories"]["cache"]["names_signs"]
    else:
        return st.session_state["api_categories"]["cache"]["names_signs"]

def get_category_data(id: str):
    """Get category data by id."""
    categories = get_or_fetch_categories_data()
    for category in categories:
        if category["id"] == id:
            return category
    return None

def get_category_id(name: str):
    """Get category id by name."""
    categories = get_or_fetch_categories_data()
    for category in categories:
        if category["name"] == name:
            return category["id"]
    return None

def get_category_sign(name: str):
    """Get category sign by id."""
    categories = get_or_fetch_categories_data()
    for category in categories:
        if category["name"] == name:
            return category["sign"]
    return None


# TRANSACTIONS CACHE UTILS
def get_or_fetch_transactions_page(page: int = 1, page_size: int = 50):
    """Get or fetch transactions page."""
    if page not in st.session_state["api_transactions"]["cache"]["by_page"]:
        update_cache(["transactions"], page=page, page_size=page_size)
        return st.session_state["api_transactions"]["cache"]["by_page"][page]
    else:
        return st.session_state["api_transactions"]["cache"]["by_page"][page]

def get_or_fetch_all_transactions():
    """Get or fetch all transactions."""    
    st.session_state["api_transactions"]["cache"]["all_transactions"] = []
    
    for page in range(1, st.session_state["api_transactions"]["cache"]["info"]["pages_count"] + 1):
        
        transactions = get_or_fetch_transactions_page(page=page, page_size=st.session_state["api_transactions"]["cache"]["info"]["page_size"])
        st.session_state["api_transactions"]["cache"]["all_transactions"].extend(transactions)
    
    return st.session_state["api_transactions"]["cache"]["all_transactions"]


# ANALYTICS CACHE UTILS
def get_or_fetch_current_analytics():
    """Get or fetch analytics current."""
    if st.session_state["api_analytics"]["cache"]["current"] == {}:
        update_cache(["current_analytics"])
        return st.session_state["api_analytics"]["cache"]["current"]
    else:
        return st.session_state["api_analytics"]["cache"]["current"]

def get_or_fetch_monthly_analytics(year: int = current_year, month: int = current_month):
    """Get or fetch analytics monthly."""
    if f"{year}-{month}" not in st.session_state["api_analytics"]["cache"]["monthly"]:
        update_cache(["monthly_analytics"], year=year, month=month)
        return st.session_state["api_analytics"]["cache"]["monthly"][f"{year}-{month}"]
    else:
        return st.session_state["api_analytics"]["cache"]["monthly"][f"{year}-{month}"]

def get_or_fetch_yearly_analytics(year: int = current_year):
    """Get or fetch analytics yearly."""
    if year not in st.session_state["api_analytics"]["cache"]["yearly"]:
        update_cache(["yearly_analytics"], year=year)
        return st.session_state["api_analytics"]["cache"]["yearly"][year]
    else:
        return st.session_state["api_analytics"]["cache"]["yearly"][year]

def get_or_fetch_historical_analytics():
    """Get or fetch analytics historical."""
    if st.session_state["api_analytics"]["cache"]["historical"] == {}:
        update_cache(["historical_analytics"])
        return st.session_state["api_analytics"]["cache"]["historical"]
    else:
        return st.session_state["api_analytics"]["cache"]["historical"]

def get_or_fetch_analytics_years():
    """Get or fetch analytics years."""
    if st.session_state["api_analytics"]["cache"]["historical"] == {}:
        update_cache(["historical_analytics"])
        return st.session_state["api_analytics"]["cache"]["years"]
    else:
        return st.session_state["api_analytics"]["cache"]["years"]


# UPDATE CACHE MANAGEMENT
def update_cache(cache_types: list[str], page: int = 1, page_size: int = 50, year: int = current_year, month: int = current_month) -> None:
    """Update specific entity data in cache after change."""
    for cache_type in cache_types:
        
        if cache_type == "user_info":
            st.session_state["api_auth"]["cache"]["user_info"] = st.session_state["api_auth"]["service"].get_user_info()

        elif cache_type == "locations":
            locations_data = st.session_state["api_locations"]["service"].get_locations_data()
            st.session_state["api_locations"]["cache"]["data"] = locations_data
            st.session_state["api_locations"]["cache"]["names"] = [location["name"] for location in locations_data]
        
        elif cache_type == "buckets":
            buckets_data = st.session_state["api_buckets"]["service"].get_buckets_data()
            st.session_state["api_buckets"]["cache"]["data"] = buckets_data
            st.session_state["api_buckets"]["cache"]["names"] = [bucket["name"] for bucket in buckets_data]
            st.session_state["api_buckets"]["cache"]["names_allocations"] = [(bucket["name"], bucket["allocation_percentage"]) for bucket in buckets_data]
            st.session_state["api_buckets"]["cache"]["total_allocation"] = sum(int(bucket["allocation_percentage"]) for bucket in buckets_data)
            st.session_state["api_buckets"]["cache"]["allocation_status"] = "COMPLETE" if st.session_state["api_buckets"]["cache"]["total_allocation"] == 100 else "INCOMPLETE"

        elif cache_type == "categories":
            categories_data = st.session_state["api_categories"]["service"].get_categories_data()
            st.session_state["api_categories"]["cache"]["data"] = categories_data
            st.session_state["api_categories"]["cache"]["names"] = [category["name"] for category in categories_data]
            st.session_state["api_categories"]["cache"]["signs"] = list({category["sign"] for category in categories_data})
            st.session_state["api_categories"]["cache"]["names_signs"] = [(category["name"], category["sign"]) for category in categories_data]

        elif cache_type == "transactions":
            st.session_state["api_transactions"]["cache"]["info"]["page_size"] = page_size
            page_data = st.session_state["api_transactions"]["service"].get_transactions_by_page(page=page, page_size=page_size)
            st.session_state["api_transactions"]["cache"]["by_page"][page] = page_data["results"]
            st.session_state["api_transactions"]["cache"]["info"]["pages_count"] = (page_data["count"] + (page_size - 1)) // page_size
            st.session_state["api_transactions"]["cache"]["info"]["transactions_count"] = page_data["count"]
            st.session_state["api_transactions"]["cache"]["info"]["has_transactions"] = st.session_state["api_transactions"]["cache"]["info"]["transactions_count"] > 0

        elif cache_type == "current_analytics":
            st.session_state["api_analytics"]["cache"]["current"] = st.session_state["api_analytics"]["service"].get_current_analytics()
        
        elif cache_type == "monthly_analytics":
            st.session_state["api_analytics"]["cache"]["monthly"][f"{year}-{month}"] = st.session_state["api_analytics"]["service"].get_monthly_analytics(year=year, month=month)

        elif cache_type == "yearly_analytics":
            st.session_state["api_analytics"]["cache"]["yearly"][year] = st.session_state["api_analytics"]["service"].get_yearly_analytics(year=year)

        elif cache_type == "historical_analytics":
            st.session_state["api_analytics"]["cache"]["historical"] = st.session_state["api_analytics"]["service"].get_historical_analytics()
            st.session_state["api_analytics"]["cache"]["years"] = st.session_state["api_analytics"]["cache"]["historical"]["yearly"].keys()

        else:
            raise ValueError(f"Invalid entity type: {cache_type}")


# CLEAR CACHE MANAGEMENT
def clear_cache(cache_types: list[str]) -> None:
    """Clear cached data for a specific entity type."""
    for cache_type in cache_types:

        if cache_type == "user_info":
            st.session_state["api_auth"]["cache"] = {}

        elif cache_type == "locations":
            st.session_state["api_locations"]["cache"] = {}
        
        elif cache_type == "buckets":
            st.session_state["api_buckets"]["cache"] = {}
        
        elif cache_type == "categories":
            st.session_state["api_categories"]["cache"] = {}
        
        elif cache_type == "transactions":
            st.session_state["api_transactions"]["cache"] = {
                "info": {},
                "by_page": {},
                "all_transactions": [],
            }

        elif cache_type == "analytics":
            st.session_state["api_analytics"]["cache"] = {
                "current": {},
                "monthly": {},
                "yearly": {},
                "historical": {},
            }
        
        elif cache_type == "current_analytics":
            st.session_state["api_analytics"]["cache"]["current"] = {}
        
        elif cache_type == "monthly_analytics":
            st.session_state["api_analytics"]["cache"]["monthly"] = {}

        elif cache_type == "yearly_analytics":
            st.session_state["api_analytics"]["cache"]["yearly"] = {}
        
        elif cache_type == "historical_analytics":
            st.session_state["api_analytics"]["cache"]["historical"] = {}

        else:
            raise ValueError(f"Invalid entity type: {cache_type}")


# CLEAR ALL CACHE
def clear_all_cache():
    """Clear all cached data."""
    clear_cache(["locations", "buckets", "categories", "transactions", "analytics"])


# CHECK FETCHED CACH
def cache_fetched(cache_types: list[str]) -> bool:
    """Check if the cache has been fetched."""
    is_fetched = True

    for cache_type in cache_types:
        
        if cache_type == "user_info":
            is_fetched = is_fetched and st.session_state["api_auth"]["cache"] != {}

        if cache_type == "locations":
            is_fetched = is_fetched and st.session_state["api_locations"]["cache"] != {}
        
        elif cache_type == "buckets":
            is_fetched = is_fetched and st.session_state["api_buckets"]["cache"] != {}
        
        elif cache_type == "categories":
            is_fetched = is_fetched and st.session_state["api_categories"]["cache"] != {}
        
        elif cache_type == "transactions":
            is_fetched = is_fetched and st.session_state["api_transactions"]["cache"] != {
                "info": {},
                "by_page": {},
                "all_transactions": {},
            }

        elif cache_type == "current_analytics":
            is_fetched = is_fetched and st.session_state["api_analytics"]["cache"]["current"] != {}
        
        elif cache_type == "monthly_analytics":
            is_fetched = is_fetched and st.session_state["api_analytics"]["cache"]["monthly"] != {}

        elif cache_type == "yearly_analytics":
            is_fetched = is_fetched and st.session_state["api_analytics"]["cache"]["yearly"] != {}
        
        elif cache_type == "historical_analytics":
            is_fetched = is_fetched and st.session_state["api_analytics"]["cache"]["historical"] != {}

        else:
            raise ValueError(f"Invalid entity type: {cache_type}")
    
    return is_fetched
