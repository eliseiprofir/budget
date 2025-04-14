import streamlit as st
import time

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("Login")
        st.write("Please login to access the Budget Management System")
        
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            if not email or not password:
                st.error("Please enter both email and password")
                return

            api = st.session_state.get('auth_api')
            api.login(email, password)
            if api.is_authenticated():
                st.session_state['authenticated'] = True
                st.success("Login successful!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid credentials")


        st.markdown("""
        ---
        Don't have an account?
        """)

        if st.button("Sign Up"):
            st.session_state["current_page"] = "signup"
            st.rerun()
