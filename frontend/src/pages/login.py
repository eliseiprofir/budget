import streamlit as st
from src.services.api import APIService

def show():
    st.title("Login")
    
    # Create columns for centering the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("Please login to access the Budget Management System")
        
        # Login form
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            if not username or not password:
                st.error("Please enter both username and password")
                return
                
            try:
                api = st.session_state.get('api')
                if not api:
                    api = APIService()
                    st.session_state['api'] = api
                
                response = api.login(username, password)
                
                if api.is_authenticated():
                    st.session_state['authenticated'] = True
                    st.success("Login successful!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")
            except Exception as e:
                st.error(f"Login failed: {str(e)}")
        
        # Add some spacing
        st.write("")
        
        # Info text
        st.markdown("""
        ---
        Don't have an account? Please contact your administrator.
        """)
