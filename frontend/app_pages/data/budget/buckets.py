import time
import streamlit as st
from utils.cache_utils import update_cache

COL1 = 4
COL2 = 4
COL3 = 3
COL4 = 3

def buckets_config():
    """Settings section for buckets."""
    
    st.subheader("🪙 Buckets")
    st.write("Configure your buckets here. You can add, edit or delete your buckets.")
    
    # Bucket API and cache
    buckets_api = st.session_state["api_buckets"]["service"]
    cache = st.session_state["api_buckets"]["cache"]
    buckets = cache["list"]
    buckets_names = cache["names"]
    allocation_status = cache["allocation_status"]
    total_allocation = cache["total_allocation"]

    # Form for adding a new bucket
    with st.form("add_bucket"):
        col1, col2 = st.columns([5, 5])
        
        new_bucket = col1.text_input("Name of the bucket")
        col1.info("Different purposes for your money (e.g. Economy, Education, Necessities, Donations).")
        new_percentage = col2.number_input("Allocation percentage", step=1)
        col2.info("The percentage of your income that will be allocated to this bucket, if you choose 'split income' feature.")
        
        submitted = st.form_submit_button("Add new bucket")
        if submitted:
            if not new_bucket:
                st.error("Psst... you forgot to enter the name.")
            elif new_bucket in buckets_names:
                st.error("This bucket already exists.")
            elif new_percentage < 0:
                st.error("Allocation percentage should be greater than 0.")
            elif new_percentage > 100 or (total_allocation + new_percentage > 100):
                st.error(f"Total allocation cannot exceed 100%. For this bucket you can have up to {100-total_allocation}%.")
            else:
                response = buckets_api.add_bucket(new_bucket, new_percentage)
                if isinstance(response, dict):
                    st.session_state["api_buckets"]["edit_buc_name"] = None
                    st.success("Bucket added!")
                    update_cache("buckets")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(response)

    # Show head of the table
    col1, col2, col3, col4 = st.columns([COL1, COL2, COL3, COL4])
    col1.markdown("**Name**")
    col2.markdown("**Allocation percentage**")
    col3.markdown("**Edit**")
    col4.markdown("**Delete**")

    # Show existing buckets
    for name, percentage in buckets:
        col1, col2, col3, col4 = st.columns([COL1, COL2, COL3, COL4])

        # Edit mode
        if st.session_state["api_buckets"]["edit_buc_name"] == name:
            buckets_names = [buc for buc in buckets_names if buc != name]
            
            new_name = col1.text_input("Edit bucket name", value=name, key=f"edit_buc_{name}")
            new_percentage = col2.number_input("Allocation percentage", step=1, value=int(percentage))
            
            if col3.button("💾 Save", key=f"save_buc_{name}"):
                if not new_name:
                    st.error("Psst... you forgot to enter the name.")
                elif new_name in buckets_names:
                    st.error("This name already exists.")
                elif new_percentage < 0:
                    st.error("Allocation percentage should be greater than 0.")
                elif new_percentage > 100 or (total_allocation - int(percentage) + new_percentage > 100):
                    st.error(f"Total allocation cannot exceed 100%. For this bucket you can have up to {100-total_allocation+int(percentage)}%.")
                else:
                    response = buckets_api.update_bucket(old_name=name, new_name=new_name, new_percentage=new_percentage)
                    if isinstance(response, dict):
                        buckets_names += [new_name]
                        st.session_state["api_buckets"]["edit_buc_name"] = None
                        st.success("Bucket updated!")
                        update_cache("buckets")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(response)

            update_cache("transactions")
            
            if col4.button("✖️ Cancel", key=f"cancel_buc_{name}"):
                st.session_state["api_buckets"]["edit_buc_name"] = None
                st.rerun()
        
        # Delete mode
        elif st.session_state["api_buckets"]["delete_buc_name"] == name:
            col1.write(name)
            col2.write(f"{percentage}%")

            # If only one bucket and transactions exist - don't allow deleting it
            if len(st.session_state["api_buckets"]["cache"]["names"]) == 1 and len(st.session_state["api_transactions"]["cache"]["list"]) > 0:
                st.warning("You cannot delete the last bucket because there are still transactions associated with it. You can rename it or delete associated transactions first.")
                
                if col4.button("✖️ Cancel", key="cancel_buc_delete"):
                    st.session_state["api_buckets"]["delete_buc_name"] = None
                    st.rerun()

            else:
                buckets_names = [buc for buc in buckets_names if buc != name]
                new_bucket = st.selectbox(label="Select another bucket to move the transactions from this one to.", options=buckets_names)
                new_bucket_id = buckets_api.get_bucket_id(new_bucket)

                st.warning(f"Are you sure you want to delete this bucket: {st.session_state['api_buckets']['delete_buc_name']}?")
                
                if col3.button("✔️ Confirm", key="confirm_buc_delete"):

                    # Move transactions to new bucket
                    st.info(f"Moving transactions to '{new_bucket}'...")
                    transactions_api = st.session_state["api_transactions"]["service"]
                    transactions = st.session_state["api_transactions"]["cache"]["list"]
                    transactions_to_move = [transaction["id"] for transaction in transactions if transaction["bucket"]["name"] == name]
                    for transaction_id in transactions_to_move:
                        response = transactions_api.update_transaction_bucket(transaction_id, new_bucket_id)
                        if not isinstance(response, dict):
                            st.error(response)
                    update_cache("transactions")

                    # Delete bucket
                    response = buckets_api.delete_bucket(st.session_state["api_buckets"]["delete_buc_name"])
                    if isinstance(response, dict):
                        st.success("Bucket deleted!")
                        update_cache("buckets")
                        st.session_state["api_buckets"]["delete_buc_name"] = None
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(response)
            
                if col4.button("✖️ Cancel", key="cancel_buc_delete"):
                    st.session_state["api_buckets"]["delete_buc_name"] = None
                    st.rerun()

        # Show mode
        else:
            col1.write(name)
            col2.write(f"{percentage}%")
            
            if col3.button("✏️ Edit", key=f"edit_buc_{name}"):
                st.session_state["api_buckets"]["edit_buc_name"] = name
                st.rerun()
            
            if col4.button("🗑️ Delete", key=f"delete_buc_{name}"):
                st.session_state["api_buckets"]["delete_buc_name"] = name
                st.rerun()
    
    # Warnings for different cases
    if allocation_status == "COMPLETE":
        st.success("Your bucket allocations are complete (100%). You can add now income transactions with 'split income' feature.")
    elif allocation_status == "INCOMPLETE":
        st.warning(f"Your bucket allocations are incomplete ({total_allocation}%). It should be 100%. Add {100-total_allocation}% to one of your buckets if you want to use 'split income' feature for income transactions.")
    else:
        st.warning("Add at least one bucket to be able to add new transactions.")
