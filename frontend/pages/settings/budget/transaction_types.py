import time
import streamlit as st

OPTIONS = ("POSITIVE", "NEGATIVE", "NEUTRAL")

COL1 = 4
COL2 = 4
COL3 = 3
COL4 = 3

def transaction_types_settings():
    """Settings section for Transaction Types."""

    st.header("📈 Transaction Types")
    st.write("Configure your transaction types here. You can add, edit or delete your transaction types.")
    
    # Transaction Type API
    transaction_types_api = st.session_state["api_transaction_types"]["service"]
    transaction_types = transaction_types_api.get_transaction_types_list()
    transaction_types_names = transaction_types_api.get_transaction_types_names()

    # Form for adding a new transaction type
    with st.form("add_transaction_type"):
        new_name = st.text_input("Name of the transaction type *")
        new_sign = st.selectbox(options=OPTIONS, label="Sign *")
        st.info("Specifies the nature of the transactions. POSITIVE: money coming in, NEGATIVE: money going out, or NEUTRAL: moving between locations/transaction_types (e.g. Income, Expense, Transfer).")
        st.warning("IMPORTANT: Sign cannot be changed after transaction type creation!")
        
        submitted = st.form_submit_button("Add new transaction type")
        if submitted:
            if not new_name:
                st.error("Psst... you forgot to enter the name.")
            elif new_name in transaction_types_names:
                st.error("This transaction type already exists.")
            else:
                response = transaction_types_api.add_transaction_type(name=new_name, sign=new_sign)
                if isinstance(response, dict):
                    st.session_state["api_transaction_types"]["edit_ttype_name"] = None
                    st.success("Transaction type added!")
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

    # Show existing transaction types
    for name, sign in transaction_types:
        col1, col2, col3, col4 = st.columns([COL1, COL2, COL3, COL4])
        
        # Edit mode
        if st.session_state["api_transaction_types"]["edit_ttype_name"] == name:
            transaction_types_names = [ttype for ttype in transaction_types_names if ttype != name]
            new_name = col1.text_input("Edit transaction type name", value=name, key=f"edit_ttype_{name}")
            col2.write(sign)
            col2.info("Sign cannot be changed")
            
            if col3.button("💾 Save", key=f"save_ttype_{name}"):
                if not new_name:
                    st.error("Psst... you forgot to enter the name.")
                elif new_name in transaction_types_names:
                    st.error("This name already exists.")
                else:
                    response = transaction_types_api.update_transaction_type_name(old_name=name, new_name=new_name)
                    if isinstance(response, dict):
                        transaction_types_names += [new_name]
                        st.session_state["api_transaction_types"]["edit_ttype_name"] = None
                        st.success("Transaction type updated!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(response)
            
            if col4.button("✖️ Cancel", key=f"cancel_ttype_{name}"):
                st.session_state["api_transaction_types"]["edit_ttype_name"] = None
                st.rerun()
        
        # Delete mode
        elif st.session_state["api_transaction_types"]["delete_ttype_name"] == name:
            col1.write(name)
            col2.write(sign)            
            st.warning(f"Are you sure you want to delete this transaction type: {st.session_state['api_transaction_types']['delete_ttype_name']}?")
            
            if col3.button("✔️ Confirm", key="confirm_ttype_delete"):
                response = transaction_types_api.delete_transaction_type(st.session_state["api_transaction_types"]["delete_ttype_name"])
                if isinstance(response, dict):
                    st.success("Transacino type deleted!")
                    st.session_state["api_transaction_types"]["delete_ttype_name"] = None
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(response)
            
            if col4.button("✖️ Cancel", key="cancel_ttype_delete"):
                st.session_state["api_transaction_types"]["delete_ttype_name"] = None
                st.rerun()
        # Show mode
        else:
            col1.write(name)
            col2.write(f"{sign}")
            
            if col3.button("✏️ Edit", key=f"edit_ttype_{name}"):
                st.session_state["api_transaction_types"]["edit_ttype_name"] = name
                st.rerun()
            
            if col4.button("🗑️ Delete", key=f"delete_ttype_{name}"):
                st.session_state["api_transaction_types"]["delete_ttype_name"] = name
                st.rerun()

    # No transaction type warning
    if len(transaction_types) < 1:
        st.warning("Add at least one transaction type to be able to add new transactions.")
