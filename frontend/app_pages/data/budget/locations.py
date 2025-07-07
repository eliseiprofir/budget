import time
import streamlit as st

from utils.cache_utils import update_cache
from utils.cache_utils import clear_cache

from utils.cache_utils import get_or_fetch_locations_names

from utils.cache_utils import get_or_fetch_all_transactions

COL1 = 8
COL2 = 3
COL3 = 3

def locations_config():
    """Settings section for locations."""

    st.subheader("🏦 Locations")
    st.write("Configure your locations here. You can add, edit or delete your locations.")

    # Location API and cache
    locations_api = st.session_state["api_locations"]["service"]
    locations = get_or_fetch_locations_names()

    # Form for adding a new location
    with st.form("add_location"):
        new_location = st.text_input("Name of the location *")
        st.info("Locations where you keep your money (e.g. Cash, ING, Revolut).")
        
        submitted = st.form_submit_button("Add new location")
        if submitted:
            if new_location in locations:
                st.error("This location already exists.")
            elif not new_location:
                st.error("Psst... you forgot to enter the name.")
            else:
                response = locations_api.add_location(new_location)
                if isinstance(response, dict):
                    st.success("Location added!")
                    update_cache(["locations"])
                    clear_cache(["analytics"])
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(response)         
    
    # Show existing locations
    for name in locations:
        col1, col2, col3 = st.columns([COL1, COL2, COL3])
        
        # Edit mode
        if st.session_state["api_locations"]["edit_loc_name"] == name:
            locations = [loc for loc in locations if loc != name]
            new_name = st.text_input("Edit location name", value=name, key=f"edit_loc_{name}")
            
            if st.button("💾 Save", key=f"save_loc_{name}"):
                if not new_name:
                    st.error("Psst... you forgot to enter the name.")
                elif new_name in locations:
                    st.error("This location already exists")
                else:
                    response = locations_api.update_location(old_name=name, new_name=new_name)
                    if isinstance(response, dict):
                        locations += [new_name]
                        st.session_state["api_locations"]["edit_loc_name"] = None
                        st.success("Location updated!")
                        update_cache(["locations"])
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(response)
            
                clear_cache(["transactions", "analytics"])
            
            if st.button("✖️ Cancel", key=f"cancel_loc_{name}"):
                st.session_state["api_locations"]["edit_loc_name"] = None
                st.rerun()
        
        # Delete mode
        elif st.session_state["api_locations"]["delete_loc_name"] == name:
            col1.write(f"Name: **{name}**")

            # If only one location and no transactions
            if len(st.session_state["api_locations"]["cache"]["names"]) == 1 and len(st.session_state["api_transactions"]["cache"]["all_transactions"]) == 0:
                st.warning(f"Are you sure you want to delete this location: **{st.session_state['api_locations']['delete_loc_name']}**?")
                
                if st.button("✔️ Confirm", key="confirm_loc_delete"):

                    # Delete location
                    response = locations_api.delete_location(st.session_state["api_locations"]["delete_loc_name"])
                    if isinstance(response, dict):
                        st.success("Location deleted!")
                        update_cache(["locations"])
                        clear_cache(["analytics"])
                        st.session_state["api_locations"]["delete_loc_name"] = None
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(response)
                
                if st.button("✖️ Cancel", key="cancel_loc_delete"):
                    st.session_state["api_locations"]["delete_loc_name"] = None
                    st.rerun()

            # If only one location and transactions exist - don't allow deleting it
            elif len(st.session_state["api_locations"]["cache"]["names"]) == 1 and len(st.session_state["api_transactions"]["cache"]["list"]) > 0:
                st.warning("You cannot delete the last location because there are still transactions associated with it. You can rename it or delete associated transactions first.")
                
                if col3.button("✖️ Cancel", key="cancel_loc_delete"):
                    st.session_state["api_locations"]["delete_loc_name"] = None
                    st.rerun()
            
            # If more than one bucket and transactions exist - move transactions to another bucket before deleting it
            else:
                locations = [loc for loc in locations if loc != name]
                new_location = st.selectbox(label="❗ Select another location to move the transactions from this one to.", options=locations)
                new_location_id = locations_api.get_location_id(new_location)

                st.warning(f"Are you sure you want to delete this location: **{st.session_state['api_locations']['delete_loc_name']}**?")
                
                if st.button("✔️ Confirm", key="confirm_loc_delete"):
                    
                    # Move transactions to new location
                    with st.spinner(f"Moving transactions to '**{new_location}**'..."):
                        transactions_api = st.session_state["api_transactions"]["service"]
                        transactions = get_or_fetch_all_transactions()
                        transactions_to_move = [transaction["id"] for transaction in transactions if transaction["location"]["name"] == name]
                        for transaction_id in transactions_to_move:
                            response = transactions_api.update_transaction_location(transaction_id, new_location_id)
                            if not isinstance(response, dict):
                                st.error(response)
                        clear_cache(["transactions", "analytics"])

                    # Delete location
                    response = locations_api.delete_location(st.session_state["api_locations"]["delete_loc_name"])
                    if isinstance(response, dict):
                        st.success("Location deleted!")
                        update_cache(["locations"])
                        st.session_state["api_locations"]["delete_loc_name"] = None
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(response)
                
                if st.button("✖️ Cancel", key="cancel_loc_delete"):
                    st.session_state["api_locations"]["delete_loc_name"] = None
                    st.rerun()

        # Show mode
        else:
            col1.write(f"Name: **{name}**")
            
            if col2.button("✏️ Edit", key=f"edit_loc_{name}"):
                st.session_state["api_locations"]["edit_loc_name"] = name
                st.rerun()
            
            if col3.button("🗑️ Delete", key=f"delete_loc_{name}"):
                st.session_state["api_locations"]["delete_loc_name"] = name
                st.rerun()
        
        st.markdown("---")

    # No locations warning
    if len(locations) < 1:
        st.warning("Add at least one location to be able to add new transactions.")
