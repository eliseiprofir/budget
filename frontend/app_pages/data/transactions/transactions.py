import time
import altair as alt
import streamlit as st
import pandas as pd

from .add_transactions import add_transactions_form

from utils.cache_utils import update_cache
from utils.cache_utils import clear_cache
from utils.cache_utils import cache_fetched

from utils.cache_utils import get_category_id
from utils.cache_utils import get_location_id
from utils.cache_utils import get_bucket_id

from utils.cache_utils import get_or_fetch_transactions_page
from utils.cache_utils import get_or_fetch_all_transactions

from utils.cache_utils import get_or_fetch_current_analytics

from app_pages.reports.current import process_current_status_data


def update_current_page(page: int):
    st.session_state["api_transactions"]["cache"]["info"]["current_page"] = page


def transactions_page():
    """Transactions page."""
    
    st.title("💸 Transaction Management")
    st.write("Here you can see, add and edit your transactions.")
    
    if st.button("🔄 Refresh data"):
        with st.spinner("Loading data..."):
            clear_cache(["transactions", "current_analytics"])
            update_cache(["transactions", "current_analytics"])
        st.rerun()
    
    if not cache_fetched(["transactions", "current_analytics"]):
        with st.spinner("Loading data..."):
            get_or_fetch_transactions_page()
            get_or_fetch_current_analytics()
    
    # Transactions API service
    transactions_api = st.session_state["api_transactions"]["service"]

    # Add transaction form
    add_transactions_form()

    # Displaying all transactions
    st.subheader("🔢 Transactions table")

    # Pagination
    show_all = st.checkbox(
        label="📋 Show all transactions",
        on_change=update_current_page(1),
    )

    if show_all:
        st.session_state["api_transactions"]["cache"]["info"]["current_transactions"] = get_or_fetch_all_transactions()
        st.info(f"All {len(st.session_state['api_transactions']['cache']['info']['current_transactions'])} transactions")
    elif not show_all:
        current_page = st.number_input(
            label="Page",
            min_value=1,
            max_value=st.session_state["api_transactions"]["cache"]["info"]["pages_count"],
            value=st.session_state["api_transactions"]["cache"]["info"]["current_page"],
        )
        st.session_state["api_transactions"]["cache"]["info"]["current_transactions"] = get_or_fetch_transactions_page(page=current_page)
        col1, col2 = st.columns(2)
        col1.info(f"Page {current_page}/{st.session_state['api_transactions']['cache']['info']['pages_count']}")
        col2.info("If some fields are empty, click on the **🔄 Refresh data** button.")

    data = []
    for transaction in st.session_state["api_transactions"]["cache"]["info"]["current_transactions"]:
        data.append({
                "🗑️ Delete": False,
                "🆔": transaction["id"],
                "📆 Date": pd.to_datetime(transaction["date"]),
                "✍️ Description": transaction["description"],
                "🔢 Amount": pd.to_numeric(transaction["amount"]),
                "🔖 Category": transaction["category"]["name"],
                "🪙 Bucket": transaction["bucket"]["name"],
                "🏦 Location": transaction["location"]["name"],
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
        "🗑️ Delete": st.column_config.CheckboxColumn("🗑️ Delete", default=False),
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

        # EDIT / DELETE MODE
        if st.session_state["api_transactions"]["edit_mode"]:
            st.warning("Editing mode on. After changes, don't forget to save (button below the table) and toggle off editing mode. If you want to discard all changes, toggle off editing mode.")
            
            # Display editable table
            new_data = st.data_editor(**edit_data_config)
            
            # Find changes
            changes = new_data.compare(data)
            deleted_indices = new_data[new_data["🗑️ Delete"] == True].index  # noqa
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
                            new_category_id = get_category_id(name=new_row["🔖 Category"])
                            new_location_id = get_location_id(name=new_row["🏦 Location"])
                            new_bucket_id = get_bucket_id(name=new_row["🪙 Bucket"])
                            response = transactions_api.update_transaction(
                                transaction_id=new_row["🆔"],
                                description=new_row["✍️ Description"],
                                category_id=new_category_id,
                                date=str(new_row["📆 Date"]),
                                amount=float(new_row["🔢 Amount"]),
                                location_id=new_location_id,
                                bucket_id=new_bucket_id,
                            )
                            if not isinstance(response, dict):
                                st.error(response)
                                break
                        st.session_state["api_transactions"]["edit_mode"] = False
                        st.success("Transaction(s) updated!")
                        
                        update_cache(["transactions"])
                        clear_cache(["analytics"])
                        
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
                            new_category_id = get_category_id(name=new_row["🔖 Category"])
                            new_location_id = get_location_id(name=new_row["🏦 Location"])
                            new_bucket_id = get_bucket_id(name=new_row["🪙 Bucket"])
                            response = transactions_api.update_transaction(
                                transaction_id=new_row["🆔"],
                                description=new_row["✍️ Description"],
                                category_id=new_category_id,
                                date=str(new_row["📆 Date"]),
                                amount=float(new_row["🔢 Amount"]),
                                location_id=new_location_id,
                                bucket_id=new_bucket_id,
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
                    
                    update_cache(["transactions"])
                    clear_cache(["analytics"])
                    
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
            
            filter_by_category = row2col1.toggle("🔖 By Category", key="filter_category", value=False)
            if filter_by_category:
                selected_categories = row2col1.multiselect("Select categories", options=data["🔖 Category"].unique())
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
            
            mode = row3col1.radio("Filter mode:", options=["AND", "OR"], horizontal=True)

            # Filtering data
            if conditions:
                # Every condition - intersection of data
                if mode == "AND":
                    row3col2.info("Filter mode \"AND\": Every condition must match.")
                    combined_conditions = conditions[0]
                    for cond in conditions[1:]:
                        combined_conditions &= cond
                # Any condition - union of data
                elif mode == "OR":
                    row3col2.info("Filter mode \"OR\": At least one condition must match.")
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

    # SUMMARY SECTION
    st.markdown("---")
    st.subheader("📊 Short summary")

    if not st.session_state["api_transactions"]["cache"]["info"]["has_transactions"]:
        st.warning("No transactions yet. Come back here when you add some transactions.")
        return

    current_status = process_current_status_data()
    
    locations_chart = current_status["locations"]["for_chart"]
    locations_table = current_status["locations"]["for_table"]
    locations_total = current_status["locations"]["total"]
    
    buckets_chart = current_status["buckets"]["for_chart"]
    buckets_table = current_status["buckets"]["for_table"]
    buckets_total = current_status["buckets"]["total"]
    
    balance_chart = current_status["balance"]["for_chart"]
    balance_table = current_status["balance"]["for_table"]
    balance_total = current_status["balance"]["total"]
    
    max_length = max(len(locations_chart), len(buckets_chart), len(balance_chart))
    chart_size = 20
    chart_height = 30 * max_length

    if locations_total == buckets_total == balance_total:
        st.metric(label="💰 Money available", value=balance_total)
    else:
        st.error("Totals are not equal")

    col1, col2, col3 = st.columns(3)

    # Locations section
    locations_chart = alt.Chart(locations_chart.reset_index(), height=chart_height).mark_bar(size=chart_size).encode(
        x=alt.X("Amount:Q", title=None),
        y=alt.Y("Location:N", title=None, sort=None, axis=alt.Axis(labelAngle=0)),
        color=alt.Color("Location:N", legend=None),
        tooltip=["Location", "Amount"]
    ).configure_axis(
        labelFontSize=16,
        titleFontSize=16
    ).configure_title(
        fontSize=25
    ).transform_filter(
        alt.datum.Location != "_total"
    )
    col1.subheader("🏦 Locations")
    col1.altair_chart(locations_chart, use_container_width=True)
    col1.dataframe(locations_table.set_index("Location"), use_container_width=True)

    # Buckets section
    buckets_chart = alt.Chart(buckets_chart.reset_index(), height=chart_height).mark_bar(size=chart_size).encode(
        x=alt.X("Amount:Q", title=None),
        y=alt.Y("Bucket:N", title=None, sort=None, axis=alt.Axis(labelAngle=0)),
        color=alt.Color("Bucket:N", legend=None),
        tooltip=["Bucket", "Amount"]
    ).configure_axis(
        labelFontSize=16,
        titleFontSize=16
    ).configure_title(
        fontSize=25
    ).transform_filter(
        alt.datum.Bucket != "_total"
    )
    col2.subheader("🪙 Buckets")
    col2.altair_chart(buckets_chart, use_container_width=True)
    col2.dataframe(buckets_table.set_index("Bucket"), use_container_width=True)

    # Balance section
    color_scale = alt.Scale(
        domain=["Positive", "Negative", "Neutral"],
        range=["#4CAF50", "#FF7F7F", "#898989"]
    )
    balance_chart = alt.Chart(balance_chart.reset_index(), height=chart_height).mark_bar(size=chart_size).encode(
        x=alt.X("Amount:Q", title=None),
        y=alt.Y("Balance:N", title=None, sort=None, axis=alt.Axis(labelAngle=0)),
        color=alt.Color("Balance:N", legend=None, scale=color_scale),
        tooltip=["Balance", "Amount"]
    ).configure_axis(
        labelFontSize=16,
        titleFontSize=16
    ).configure_title(
        fontSize=25
    ).transform_filter(
        alt.datum.Balance != "_total"
    )
    col3.subheader("⚖️ Balance")
    col3.altair_chart(balance_chart, use_container_width=True)
    col3.dataframe(balance_table.set_index("Balance"), use_container_width=True)
