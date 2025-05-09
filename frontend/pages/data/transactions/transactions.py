import time
import streamlit as st
import pandas as pd

from .add_transactions import add_transactions_form

from utils.cache_utils import update_cache
from utils.cache_utils import clear_all_cache
from utils.cache_utils import fetch_and_cache_data


def transactions_page():
    """Transactions page."""
    
    st.header("💸 Transactions")
    st.write("Here you can manage your transactions.")
    
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

    # Add form visibility control
    def toggle_add_transaction_form():
        st.session_state["api_transactions"]["add_form"] = not st.session_state["api_transactions"]["add_form"]  
    st.button("➕ Add transaction", on_click=toggle_add_transaction_form)
    if st.session_state["api_transactions"]["add_form"]:
        add_transactions_form()

    # Displaying all transactions
    st.subheader("🔢 All transactions")

    data = []
    for transaction in transactions:
        data.append(
            {   "🆔": transaction["id"],
                "📆 Date": pd.to_datetime(transaction["date"]),
                "✍️ Description": transaction["description"],
                "🔢 Amount": pd.to_numeric(transaction["amount"]),
                "🔖 Category": transaction["category"]["name"],
                "🪙 Bucket": transaction["bucket"]["name"],
                "🏦 Location": transaction["location"]["name"],
                "🗑️ Delete": False,
            }
        )
    
    data = pd.DataFrame(data)
    show_column_order = (
        "📆 Date", "✍️ Description", "🔢 Amount",
        "🔖 Category", "🪙 Bucket", "🏦 Location"
    )
    edit_column_order = (
        "🗑️ Delete", "📆 Date", "✍️ Description", "🔢 Amount",
        "🔖 Category", "🪙 Bucket", "🏦 Location",
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
        "🗑️ Delete": st.column_config.CheckboxColumn("🗑️ Delete", default=False)
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
        # Toggle buttons for edit and filter modes
    
        def toggle_edit_mode():
            st.session_state["api_transactions"]["edit_mode"] = not st.session_state["api_transactions"]["edit_mode"]

        def toggle_filter_mode():
            st.session_state["api_transactions"]["filter_mode"] = not st.session_state["api_transactions"]["filter_mode"]
        col1, col2 = st.columns(2)
        col1.toggle(
            "Edit mode",
            key="edit_mode",
            value=st.session_state["api_transactions"]["edit_mode"],
            on_change=toggle_edit_mode
        )
        col1.write("Edit or delete multiple transactions at once.")

        col2.toggle(
            "Filter mode",
            key="filter_mode",
            value=st.session_state["api_transactions"]["filter_mode"],
            on_change=toggle_filter_mode,
        )
        col2.write("See only transactions you are interested in.")

        # EDIT / Delete MODE
        if st.session_state["api_transactions"]["edit_mode"]:
            st.warning("Editing mode on. After changes, don't forget to save (button below the table) and toggle off editing mode.")
            
            # Display editable table
            new_data = st.data_editor(**edit_data_config)
            
            # Find changes
            changes = new_data.compare(data)
            deleted_indices = new_data[new_data["🗑️ Delete"] == True].index
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
        
        # FILTER MODE
        elif st.session_state["api_transactions"]["filter_mode"]:
            st.subheader("Filters")
            container = st.container(border=True)

            row1, row2, row3 = container.container(), container.container(), container.container()

            row1col1, row1col2, row1col3 = row1.columns(3)
            row2col1, row2col2, row2col3 = row2.columns(3)
            row3col1, row3col2, row3col3 = row3.columns(3)
            
            conditions = []

            filter_by_description = row1col1.toggle("✍️ By Description", key="filter_description", value=False)
            if filter_by_description:
                search_term = row1col1.text_input("Search:", )
                conditions.append(data["✍️ Description"].str.contains(search_term))
            
            filter_by_type = row2col1.toggle("📈 By Type", key="filter_type", value=False)
            if filter_by_type:
                selected_types = row2col1.multiselect("Select types", options=data["📈 Type"].unique())
                conditions.append(data["📈 Type"].isin(selected_types))
            
            filter_by_category = row3col1.toggle("🔖 By Category", key="filter_category", value=False)
            if filter_by_category:
                selected_categories = row3col1.multiselect("Select categories", options=data["🔖 Category"].unique())
                conditions.append(data["🔖 Category"].isin(selected_categories))

            filter_by_bucket = row1col2.toggle("🪙 By Bucket", key="filter_bucket", value=False)
            if filter_by_bucket:
                selected_buckets = row1col2.multiselect("Select buckets", options=data["🪙 Bucket"].unique())
                conditions.append(data["🪙 Bucket"].isin(selected_buckets))
            
            filter_by_location = row2col2.toggle("🏦 By Location", key="filter_location", value=False)
            if filter_by_location:
                selected_locations = row2col2.multiselect("Select locations", options=data["🏦 Location"].unique())
                conditions.append(data["🏦 Location"].isin(selected_locations))

            filter_by_date = row1col3.toggle("📅 By Date", key="filter_date", value=False)
            if filter_by_date:
                colA, colB = row1col3.columns(2)
                max_date = data["📆 Date"].max()
                min_date = data["📆 Date"].min()
                filter_date_from = colA.date_input("From:", min_value=min_date, max_value=max_date)
                filter_date_to = colB.date_input("To:", min_value=min_date, max_value=max_date)
                conditions.append((data["📆 Date"] >= str(filter_date_from)) & (data["📆 Date"] <= str(filter_date_to)))
            
            filter_by_amount = row2col3.toggle("🔢 By Amount", key="filter_amount", value=False)
            if filter_by_amount:
                min_amount = int(data["🔢 Amount"].min())-1
                max_amount = int(data["🔢 Amount"].max())+1
                amount_range = row2col3.slider(
                    "Amount range:",
                    min_value=min_amount,
                    max_value=max_amount,
                    value=(min_amount, max_amount),
                    step=1
                )
                conditions.append((data["🔢 Amount"] >= amount_range[0]) & (data["🔢 Amount"] <= amount_range[1]))
            
            mode = row3col2.radio("Filter mode:", options=["AND", "OR"], horizontal=True)

            # Filtering data
            if conditions:
                # Every condition - intersection of data
                if mode == "AND":
                    row3col3.info("Filter mode \"AND\": Every condition must match.")
                    combined_conditions = conditions[0]
                    for cond in conditions[1:]:
                        combined_conditions &= cond
                # Any condition - union of data
                elif mode == "OR":
                    row3col3.info("Filter mode \"OR\": At least one condition must match.")
                    combined_conditions = conditions[0]
                    for cond in conditions[1:]:
                        combined_conditions |= cond
                filtered_data = data[combined_conditions]
            else:
                # If no conditions, display original data
                filtered_data = data.copy()
            
            # Applying filters on the data
            if st.button("Apply filters"):
                if not conditions:
                    st.info("No filters applied. Showing all data.")
                filter_data_config = {
                    "data": filtered_data,
                    "column_config": column_config,
                    "column_order": show_column_order,
                    "use_container_width": True,
                    "hide_index": True,
                }
                # Show filtered data
                st.dataframe(**filter_data_config)
            else:
                # Original data visible for user while editing filters
                st.dataframe(**show_data_config)
        
        # SHOW MODE
        else:
            st.dataframe(**show_data_config)
