import time
import streamlit as st

from utils.cache_utils import fetch_and_cache_data


def add_transactions():
    """Transactions page."""

    # Transactions API and cache
    transactions_api = st.session_state["api_transactions"]["service"]

    # Other services
    categories_api = st.session_state["api_categories"]["service"]
    locations_api = st.session_state["api_locations"]["service"]
    buckets_api = st.session_state["api_buckets"]["service"]

    fetch_and_cache_data()

    # Form for adding a new transaction
    st.subheader("✍️ Add transaction")
    st.write("Add a new transaction below.")
    with st.form("add_transaction"):
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        description = col1.text_input("✍️ Description", key="description")
        
        category = col2.selectbox("🔖 Category", key="category", options=st.session_state["api_categories"]["cache"]["names"])
        category = categories_api.get_category_id(category_name=category)
        transaction_type = categories_api.get_category_type_sign(category_id=category)

        date = col3.date_input("📆 Date", key="date")
        amount = col3.number_input("🔢 Amount", key="amount")
        
        bucket = col4.selectbox("🪙Bucket", key="bucket", options=st.session_state["api_buckets"]["cache"]["names"])
        bucket = buckets_api.get_bucket_id(bucket_name=bucket)
        
        location = col4.selectbox("🏦 Location", key="location", options=st.session_state["api_locations"]["cache"]["names"])
        location = locations_api.get_location_id(location_name=location)
        
        split_income = col2.checkbox("Split income", key="split_income", value=False)
        is_allocation_complete: str = buckets_api.get_allocation_status()

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
                    category=category,
                    date=str(date),
                    amount=float(amount),
                    location=location,
                    bucket=bucket,
                    split_income=split_income,
                )
                if isinstance(response, dict):
                    st.success("Transaction added!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(response)
