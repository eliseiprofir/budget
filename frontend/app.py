import streamlit as st
from src.services.api import APIService
from src.pages import login

# Page config
st.set_page_config(
    page_title="Budget Management System",
    page_icon="💰",
    layout="wide"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'api' not in st.session_state:
    st.session_state['api'] = APIService()

def main():
    if not st.session_state['authenticated']:
        login.show()
    else:
        # Sidebar for navigation
        with st.sidebar:
            st.title("Navigation")
            if st.button("Logout"):
                st.session_state['api'].logout()
                st.session_state['authenticated'] = False
                st.rerun()
        
        # Main content
        st.title("Budget Management System")
        st.write("Welcome! You are now logged in.")
        # Here we'll add more content later

if __name__ == "__main__":
    main()