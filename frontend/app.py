import streamlit as st

from services.auth import AuthAPIService
from services.locations import LocationsAPIService
from services.buckets import BucketsAPIService
from services.transaction_types import TransactionTypesAPIService
from services.categories import CategoriesAPIService

from pages.auth.login import login_page
from pages.auth.signout import signout_page
from pages.auth.signup import signup_page
from pages.settings.account import account_settings_page
from pages.settings.budget.budget import budget_settings_page

st.set_page_config(
    page_title="Budget Management System",
    page_icon="💰",
    layout="wide"
)

# Initialize session state variables and services
if "api_auth" not in st.session_state:
    st.session_state["api_auth"] = {
        "service": None,
        "base_url": "http://backend:8000/api",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": None,
        },
        "token": None,
        "authenticated": False,
        "user_id": None
    }
    st.session_state["api_auth"]["service"] = AuthAPIService()

if "api_locations" not in st.session_state:
    st.session_state["api_locations"] = {
        "service": None,
        "edit_loc_name": None,
        "delete_loc_name": None,
    }
    st.session_state["api_locations"]["service"] = LocationsAPIService()

if "api_buckets" not in st.session_state:
    st.session_state["api_buckets"] = {
        "service": None,
        "edit_buc_name": None,
        "delete_buc_name": None,
    }
    st.session_state["api_buckets"]["service"] = BucketsAPIService()

if "api_transaction_types" not in st.session_state:
    st.session_state["api_transaction_types"] = {
        "service": None,
        "edit_ttype_name": None,
        "delete_ttype_name": None,
    }
    st.session_state["api_transaction_types"]["service"] = TransactionTypesAPIService()

if "api_categories" not in st.session_state:
    st.session_state["api_categories"] = {
        "service": None,
        "edit_cat_name": None,
        "delete_cat_name": None,
    }
    st.session_state["api_categories"]["service"] = CategoriesAPIService()

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "login"

# Define pages
login = st.Page(login_page, title="Login", icon="🔑")
signout = st.Page(signout_page, title="Sign Out", icon="🚪")
signup = st.Page(signup_page, title="Sign Up", icon="👤")

budget_settings = st.Page(budget_settings_page, title="Budget Configuration", icon="💰")
account_settings = st.Page(account_settings_page, title="Edit Account", icon="👤")

# Navigation logic
if st.session_state["api_auth"]["authenticated"]:
    pg = st.navigation({
        "Settings": [budget_settings, account_settings, signout],
    })
else:
    if st.session_state.current_page == "signup":
        pg = st.navigation([signup])
    else:
        pg = st.navigation([login])

pg.run()
