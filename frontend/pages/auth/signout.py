import time
import streamlit as st

def signout_page():
    st.title("Sign Out")
    st.write("Click the button below to sign out.")
    
    if st.button("Sign Out", use_container_width=True):
        st.session_state["api_auth"]["service"].logout()
        st.session_state["api_auth"]["authenticated"] = False
        st.success("Sign Out successful!")
        time.sleep(1)
        st.rerun()
