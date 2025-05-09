import time
import streamlit as st
from utils.cache_utils import update_cache

OPTIONS = ("POSITIVE", "NEGATIVE", "NEUTRAL")

COL1 = 4
COL2 = 4
COL3 = 3
COL4 = 3

def categories_config():
    """Settings section for Categories."""

    st.subheader("🔖 Categories")
    st.write("Configure your categories here. You can add, edit or delete your categories.")
    
    # Category API and cache
    categories_api = st.session_state["api_categories"]["service"]
    cache = st.session_state["api_categories"]["cache"]
    categories = cache["list"]
    categories_names = cache["names"]

    # Form for adding a new category
    with st.form("add_category"):
        new_name = st.text_input("Name of the category *")
        new_sign = st.selectbox(options=OPTIONS, label="Sign *")
        st.info("Specifies the category of the transactions. (e.g. for Income (positive) transactions: Salary, Bonuses; for Expense (negative) transactions: Utilities, Food, Courses, Books, Gas).")
        
        submitted = st.form_submit_button("Add new category")
        if submitted:
            if not new_name:
                st.error("Psst... you forgot to enter the name.")
            elif new_name in categories_names:
                st.error("This category already exists.")
            else:
                response = categories_api.add_category(name=new_name, sign=new_sign)
                if isinstance(response, dict):
                    st.session_state["api_categories"]["edit_cat_name"] = None
                    st.success("category added!")
                    update_cache("categories")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(response)        

    # Show head of the table
    col1, col2, col3, col4 = st.columns([COL1, COL2, COL3, COL4])
    col1.markdown("**Name**")
    col2.markdown("**Sign**")
    col3.markdown("**Edit**")
    col4.markdown("**Delete**")

    # Show existing categories
    for name, transaction_type in categories:
        col1, col2, col3, col4 = st.columns([COL1, COL2, COL3, COL4])
        
        # Edit mode
        if st.session_state["api_categories"]["edit_cat_name"] == name:
            categories_names = [cat for cat in categories_names if cat != name]
            new_name = col1.text_input("Edit category name", value=name, key=f"edit_cat_{name}")
            new_sign = col2.selectbox(
                options=OPTIONS,
                label="Sign *",
                key=f"edit_{name}",
                index=OPTIONS.index(transaction_type)
            )
            
            if col3.button("💾 Save", key=f"save_cat_{name}"):
                if not new_name:
                    st.error("Psst... you forgot to enter the name.")
                elif new_name in categories_names:
                    st.error("This name already exists.")
                else:
                    response = categories_api.update_category(old_name=name, new_name=new_name, new_sign=new_sign)
                    if isinstance(response, dict):
                        categories_names += [new_name]
                        st.session_state["api_categories"]["edit_cat_name"] = None
                        st.success("Category updated!")
                        update_cache("categories")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(response)
            
            if col4.button("✖️ Cancel", key=f"cancel_cat_{name}"):
                st.session_state["api_categories"]["edit_cat_name"] = None
                st.rerun()

        # Delete mode
        elif st.session_state["api_categories"]["delete_cat_name"] == name:
            col1.write(name)
            col2.write(transaction_type)
            st.warning(f"Are you sure you want to delete this category: {st.session_state['api_categories']['delete_cat_name']}?")
            
            if col3.button("✔️ Confirm", key="confirm_cat_delete"):
                response = categories_api.delete_category(st.session_state["api_categories"]["delete_cat_name"])
                if isinstance(response, dict):
                    st.success("Transaction type deleted!")
                    update_cache("categories")
                    st.session_state["api_categories"]["delete_cat_name"] = None
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(response)
            
            if col4.button("✖️ Cancel", key="cancel_cat_delete"):
                st.session_state["api_categories"]["delete_cat_name"] = None
                st.rerun()
        
        # Show mode
        else:
            col1.write(name)
            col2.write(transaction_type)
            
            if col3.button("✏️ Edit", key=f"edit_cat_{name}"):
                st.session_state["api_categories"]["edit_cat_name"] = name
                st.rerun()
            
            if col4.button("🗑️ Delete", key=f"delete_cat_{name}"):
                st.session_state["api_categories"]["delete_cat_name"] = name
                st.rerun()

    # No category warning
    if len(categories) < 1:
        st.warning("Add at least one category to be able to add new transactions.")
