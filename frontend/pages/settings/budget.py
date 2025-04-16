import time
import streamlit as st

def budget_settings_page():
    """Settings page for budget application."""

    st.title("💰 Budget Configuration")

    st.header("Locations")
    st.write("Configure your locations here. You can add, edit or delete your locations.")

    location_api = st.session_state["api_locations"]["service"]
    locations = location_api.get_locations_list()

    with st.form("add_location"):
        new_location = st.text_input("Name of the location *")
        submitted = st.form_submit_button("Add new location")
        if submitted:
            if new_location in locations:
                st.error("This location already exists.")
            elif new_location:
                location_api.add_location(new_location)
                st.rerun()
            else:
                st.error("Psst... you forgot to enter the name.")

    for name in locations:
        col1, col2, col3 = st.columns([8, 3, 3])

        if st.session_state["api_locations"]["edit_name"] == name:
            new_name = col1.text_input("Edit location name", value=name, key=f"edit_{name}")
            if col2.button("💾 Save", key=f"save_{name}"):
                location_api.update_location(old_name=name, new_name=new_name)
                st.session_state["api_locations"]["edit_name"] = None
                st.success("Location updated!")
                time.sleep(0.5)
                st.rerun()
            if col3.button("✖️ Cancel", key=f"cancel_{name}"):
                st.session_state["api_locations"]["edit_name"] = None
                st.rerun()
        else:
            col1.write(name)
            if col2.button("✏️ Edit", key=f"edit_{name}"):
                st.session_state["api_locations"]["edit_name"] = name
                st.rerun()
            if col3.button("🗑️ Delete", key=f"delete_{name}"):
                st.session_state["api_locations"]["delete_name"] = name
                st.rerun()

    if st.session_state["api_locations"]["delete_name"] is not None:
        st.warning(f"Are you sure you want to delete this location: {st.session_state['api_locations']['delete_name']}?")
        colA, colB = st.columns(2)
        if colA.button("Yes, delete!", key="confirm_delete"):
            location_api.delete_location(st.session_state["api_locations"]["delete_name"])
            st.success("Location deleted!")
            st.session_state["api_locations"]["delete_name"] = None
            time.sleep(0.5)
            st.rerun()
        if colB.button("No, I changed my mind!", key="cancel_delete"):
            st.session_state["api_locations"]["delete_name"] = None
            st.rerun()

