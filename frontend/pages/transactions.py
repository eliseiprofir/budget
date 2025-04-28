import time
import streamlit as st
import pandas as pd

from utils.cache_utils import update_cache
from utils.cache_utils import clear_all_cache
from utils.cache_utils import fetch_and_cache_data


def transactions_page():
    """Transactions page."""
    
    st.header("💸 Transactions")
    st.write("Here you will find all your transactions. You can add new ones, or edit and delete existing ones.")

    if st.button("🔄 Refresh data"):
        clear_all_cache()
        fetch_and_cache_data()
        st.rerun()

    # Transactions API and cache
    transactions_api = st.session_state["api_transactions"]["service"]
    transactions = transactions_api.get_transactions()

    # Other services
    categories_api = st.session_state["api_categories"]["service"]
    locations_api = st.session_state["api_locations"]["service"]
    buckets_api = st.session_state["api_buckets"]["service"]

    fetch_and_cache_data()

    # Form for adding a new transaction
    st.subheader("✍️ Add transaction")
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

    # Displaying all transactions
    st.subheader("🔢 All transactions")

    data = []
    for transaction in transactions:
        data.append(
            {   "🆔": transaction["id"],
                "📆 Date": pd.to_datetime(transaction["date"]),
                "✍️ Description": transaction["description"],
                "🔢 Amount": transaction["amount"],
                "📈 Type": transaction["transaction_type"],
                "🔖 Category": transaction["category"]["name"],
                "🪙 Bucket": transaction["bucket"]["name"],
                "🏦 Location": transaction["location"]["name"],
                "DELETE": False,
            }
        )
    
    data = pd.DataFrame(data)
    show_column_order = (
        "📆 Date", "✍️ Description", "🔢 Amount",
        "📈 Type","🔖 Category", "🪙 Bucket", "🏦 Location"
    )
    edit_column_order = (
        "DELETE", "📆 Date", "✍️ Description", "🔢 Amount",
        "📈 Type","🔖 Category", "🪙 Bucket", "🏦 Location",
    )

    column_config = {
        "🆔": st.column_config.TextColumn("🆔", width="small"),
        "📆 Date": st.column_config.DatetimeColumn(
            "📆 Date",
            format="ddd, D MMM YYYY",
            required=True,
        ),
        "✍️ Description": st.column_config.TextColumn(
            "✍️ Description",
            required=True,
            validate=r".+"
        ),
        "🔢 Amount": st.column_config.NumberColumn(
            "🔢 Amount",
            required=True,
        ),
        "📈 Type": st.column_config.TextColumn("📈 Type", disabled=True),
        "🔖 Category": st.column_config.SelectboxColumn(
            "🔖 Category",
            options=st.session_state["api_categories"]["cache"]["names"],
            required=True,
        ),
        "🪙 Bucket": st.column_config.SelectboxColumn(
            "🪙 Bucket",
            options=st.session_state["api_buckets"]["cache"]["names"],
            required=True,
        ),
        "🏦 Location": st.column_config.SelectboxColumn(
            "🏦 Location",
            options=st.session_state["api_locations"]["cache"]["names"],
            required=True,
        ),
        "DELETE": st.column_config.CheckboxColumn("DELETE", width="small", default=False)
    }

    edit_data_config = {
        "data": data,
        "column_config": column_config,
        "column_order": edit_column_order,
        "use_container_width": True,
        "hide_index": True,
    }
    
    show_data_config = {
        "data": data,
        "column_config": column_config,
        "column_order": show_column_order,
        "use_container_width": True,
        "hide_index": True,
    }

    if data.empty:
        st.info("No transactions. Add your first transaction above.")
   
    else:
        def toggle_edit_mode():
            st.session_state["api_transactions"]["edit_mode"] = not st.session_state["api_transactions"]["edit_mode"]

        st.toggle(
            "Edit transactions",
            key="edit_mode",
            value=st.session_state["api_transactions"]["edit_mode"],
            on_change=toggle_edit_mode
        )

        # Edit & delete mode on
        if st.session_state["api_transactions"]["edit_mode"]:
            st.warning("Editing mode on. After changes, don't forget to save (button below the table) and toggle off editing mode.")
            
            # Display editable table
            new_data = st.data_editor(**edit_data_config)
            
            # Find changes
            changes = new_data.compare(data)
            deleted_indices = new_data[new_data["DELETE"] == True].index
            modified_indices = changes.index.get_level_values(0).unique()
            modified_indices = [idx for idx in modified_indices if idx not in deleted_indices]
            
            # Normal edit/delete mode
            if not st.session_state["api_transactions"]["confirm_delete"]:
                
                if st.button("💾 Save changes"):
                    
                    # Case 1: Something to delete only - save data for confirmation
                    if len(deleted_indices) > 0:
                        st.session_state["api_transactions"]["confirm_delete"] = True
                        st.session_state["api_transactions"]["to_delete"] = deleted_indices
                        st.session_state["api_transactions"]["to_update"] = modified_indices
                        st.session_state["api_transactions"]["new_data"] = new_data
                        st.rerun()
                    
                    # Case 2: Something to modify only - apply them directly
                    elif len(modified_indices) > 0:
                        for index in modified_indices:
                            new_row = new_data.loc[index].to_dict()
                            new_category_id = categories_api.get_category_id(category_name=new_row["🔖 Category"])
                            new_location_id = locations_api.get_location_id(location_name=new_row["🏦 Location"])
                            new_bucket_id = buckets_api.get_bucket_id(bucket_name=new_row["🪙 Bucket"])
                            response = transactions_api.update_transaction(
                                transaction_id=new_row["🆔"],
                                description=new_row["✍️ Description"],
                                category=new_category_id,
                                date=str(new_row["📆 Date"]),
                                amount=float(new_row["🔢 Amount"]),
                                location=new_location_id,
                                bucket=new_bucket_id,
                            )
                            if not isinstance(response, dict):
                                st.error(response)
                                break
                        st.session_state["api_transactions"]["edit_mode"] = False
                        st.success("Transaction(s) updated!")
                        update_cache("transactions")
                        time.sleep(1)
                        st.rerun()

                    # Case 4: Nothing changed - do nothing
                    else:
                        st.info("No changes made.")
            
            # Case 3: Something to delete and possibly something to modify - display confirmation message
            else:
                st.warning("⚠️ You checked some transactions for deletion. Are you sure? This action cannot be undone!")
                
                if st.button("✔️ Confirm deletion and save all changes"):
                    
                    # Case 1 & 3: Apply deletions
                    for index in st.session_state["api_transactions"]["to_delete"]:
                        transaction_id = data.loc[index].to_dict()["🆔"]
                        transactions_api.delete_transaction(transaction_id=transaction_id)
                    
                    # Case 1 & 3: Apply modifications, if any
                    if len(st.session_state["api_transactions"]["to_update"]) > 0:
                        for index in st.session_state["api_transactions"]["to_update"]:
                            new_row = st.session_state["api_transactions"]["new_data"].loc[index].to_dict()
                            new_category_id = categories_api.get_category_id(category_name=new_row["🔖 Category"])
                            new_location_id = locations_api.get_location_id(location_name=new_row["🏦 Location"])
                            new_bucket_id = buckets_api.get_bucket_id(bucket_name=new_row["🪙 Bucket"])
                            response = transactions_api.update_transaction(
                                transaction_id=new_row["🆔"],
                                description=new_row["✍️ Description"],
                                category=new_category_id,
                                date=str(new_row["📆 Date"]),
                                amount=float(new_row["🔢 Amount"]),
                                location=new_location_id,
                                bucket=new_bucket_id,
                            )
                            if not isinstance(response, dict):
                                st.error(response)
                                break
                    
                    st.success("All changes applied successfully!")
                    
                    # Reset state
                    st.session_state["api_transactions"]["confirm_delete"] = False
                    st.session_state["api_transactions"]["to_delete"] = None
                    st.session_state["api_transactions"]["to_update"] = None
                    st.session_state["api_transactions"]["new_data"] = None
                    st.session_state["api_transactions"]["edit_mode"] = False
                    
                    update_cache("transactions")
                    time.sleep(1)
                    st.rerun()
                
                if st.button("✖️ Cancel"):
                    # Reset confirmation state
                    st.session_state["api_transactions"]["confirm_delete"] = False
                    st.session_state["api_transactions"]["to_delete"] = None
                    st.session_state["api_transactions"]["to_update"] = None
                    st.session_state["api_transactions"]["new_data"] = None
                    st.session_state["api_transactions"]["edit_mode"] = False
                    st.rerun()
        
        # Show mode
        else:
            st.dataframe(**show_data_config)