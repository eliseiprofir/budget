import time
import streamlit as st
from utils.cache_utils import update_cache

COL1 = 8
COL2 = 3
COL3 = 3


def locations_config():
    """Settings section for locations."""

    st.subheader("🏦 Locations")
    st.write("Configure your locations here. You can add, edit or delete your locations.")

    # Location API and cache
    locations_api = st.session_state["api_locations"]["service"]
    cache = st.session_state["api_locations"]["cache"]
    locations = cache["names"]

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
                    update_cache("locations")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(response)         
    
    # Show head of the table
    col1, col2, col3 = st.columns([COL1, COL2, COL3])
    col1.markdown("**Name**")
    col2.markdown("**Edit**")
    col3.markdown("**Delete**")

    # Show existing locations
    for name in locations:
        col1, col2, col3 = st.columns([COL1, COL2, COL3])
        
        # Edit mode
        if st.session_state["api_locations"]["edit_loc_name"] == name:
            locations = [loc for loc in locations if loc != name]
            
            new_name = col1.text_input("Edit location name", value=name, key=f"edit_loc_{name}")
            
            if col2.button("💾 Save", key=f"save_loc_{name}"):
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
                        locations_api._clear_cache()
                        update_cache("locations")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(response)
            
            update_cache("transactions")
            
            if col3.button("✖️ Cancel", key=f"cancel_loc_{name}"):
                st.session_state["api_locations"]["edit_loc_name"] = None
                st.rerun()
        
        # Delete mode
        elif st.session_state["api_locations"]["delete_loc_name"] == name:
            col1.write(name)
            st.warning(f"Are you sure you want to delete this location: {st.session_state['api_locations']['delete_loc_name']}?")
            
            if col2.button("✔️ Confirm", key="confirm_loc_delete"):
                response = locations_api.delete_location(st.session_state["api_locations"]["delete_loc_name"])
                if isinstance(response, dict):
                    st.success("Location deleted!")
                    update_cache("locations")
                    st.session_state["api_locations"]["delete_loc_name"] = None
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(response)
            
            if col3.button("✖️ Cancel", key="cancel_loc_delete"):
                st.session_state["api_locations"]["delete_loc_name"] = None
                st.rerun()

        # Show mode
        else:
            col1.write(name)
            
            if col2.button("✏️ Edit", key=f"edit_loc_{name}"):
                st.session_state["api_locations"]["edit_loc_name"] = name
                st.rerun()
            
            if col3.button("🗑️ Delete", key=f"delete_loc_{name}"):
                st.session_state["api_locations"]["delete_loc_name"] = name
                st.rerun()

    # No locations warning
    if len(locations) < 1:
        st.warning("Add at least one location to be able to add new transactions.")
