import time
import streamlit as st

from utils.cache_utils import get_location_id
from utils.cache_utils import get_or_fetch_locations_names

from utils.cache_utils import get_or_fetch_buckets_names
from utils.cache_utils import get_bucket_id
from utils.cache_utils import get_or_fetch_buckets_allocation_status

from utils.cache_utils import get_category_data
from utils.cache_utils import get_category_id
from utils.cache_utils import get_category_sign
from utils.cache_utils import get_or_fetch_categories_names

from utils.cache_utils import update_cache
from utils.cache_utils import clear_cache


def add_transactions_form():
    """Transactions page."""

    # Transactions API and cache
    transactions_api = st.session_state["api_transactions"]["service"]

    categories = get_or_fetch_categories_names()
    buckets = get_or_fetch_buckets_names()
    locations = get_or_fetch_locations_names()

    if len(locations) < 1:
        st.warning("🏦 No locations found. 🧐 Please create at least one before adding transactions. You can do this on \"Budget Configuration\" page.")
        return
    elif len(buckets) < 1:
        st.warning("🪙 No buckets found. 🧐 Please create at least one before adding transactions. You can do this on \"Budget Configuration\" page.")
        return
    elif len(categories) < 1:
        st.warning("🔖 No categories found. 🧐 Please create at least one before adding transactions. You can do this on \"Budget Configuration\" page.")
        return

    # Form for adding a new transaction
    st.subheader("✍️ Add transaction")
    st.write("Add a new transaction below.")
    with st.form("add_transaction"):
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        description = col1.text_input("✍️ Description", key="description")
        
        category_name = col2.selectbox("🔖 Category", key="category", options=categories)
        category_id = get_category_id(name=category_name)
        transaction_type = get_category_sign(name=category_name)
        category_data = get_category_data(id=category_id)

        date = col3.date_input("📆 Date", key="date")
        amount = col3.number_input("🔢 Amount", key="amount")
        
        bucket_name = col4.selectbox("🪙Bucket", key="bucket", options=buckets)
        bucket_id = get_bucket_id(name=bucket_name)
        
        location_name = col4.selectbox("🏦 Location", key="location", options=locations)
        location_id = get_location_id(name=location_name)
        
        split_income = col2.checkbox("Split income", key="split_income", value=False)
        is_allocation_complete: str = get_or_fetch_buckets_allocation_status()

        submitted = col1.form_submit_button("Add transaction", use_container_width=True)
        if submitted:
            if transaction_type != "POSITIVE" and split_income is True:
                st.error("Split income feature only available for positive transactions. Please uncheck the box or change the category.")
            elif is_allocation_complete == "INCOMPLETE" and split_income is True:
                st.error("Split income feature only available when bucket allocations are complete (100%). Please go to 'Budget Configuration' page and complete your bucket allocations or uncheck the box.") 
            elif not description:
                st.error("Please enter a description.")
            else:
                response = transactions_api.add_transaction(
                    description=description,
                    category=category_id,
                    date=str(date),
                    amount=float(amount),
                    location=location_id,
                    bucket=bucket_id,
                    split_income=split_income,
                )
                if isinstance(response, dict):
                    st.success("Transaction added!")
                    clear_cache(["transactions", "analytics"])
                    update_cache(["transactions"])
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(response)
            
            
