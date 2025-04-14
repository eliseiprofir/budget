import streamlit as st
from services.auth_api import AuthAPIService
from pages.auth.login import login_page
from pages.auth.signout import signout_page
from pages.auth.signup import signup_page
from pages.settings.account import settings_account_page

st.set_page_config(
    page_title="Budget Management System",
    page_icon="💰",
    layout="wide"
)

# Initialize session state variables
if "auth_api" not in st.session_state:
    st.session_state["auth_api"] = AuthAPIService()
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "login"

# Define pages
login = st.Page(login_page, title="Login", icon="🔑")
signout = st.Page(signout_page, title="Sign Out", icon="🚪")
signup = st.Page(signup_page, title="Sign Up", icon="👤")
# dashboard = st.Page(settings_account_page, title="Dashboard", icon="📊", default=True)
account_settings = st.Page(settings_account_page, title="Edit Account", icon="👤")

# Navigation logic
if st.session_state["authenticated"]:
    pg = st.navigation({
        # "Main": [dashboard],
        # "Settings": [account_settings],
        "Settings": [account_settings, signout],
    })
else:
    # Use current_page to determine which page to show
    if st.session_state["current_page"] == "signup":
        pg = st.navigation([signup])
    else:
        pg = st.navigation([login])

pg.run()
