import os
import streamlit as st

from services.auth import AuthAPIService
from services.locations import LocationsAPIService
from services.buckets import BucketsAPIService
from services.categories import CategoriesAPIService
from services.transactions import TransactionAPIService
from services.analytics import AnalyticsAPIService

from pages.account.auth_login import login_page
from pages.account.auth_signup import signup_page
from pages.account.auth_signout import signout_page
from pages.account.settings import account_settings_page

from pages.data.budget.config import budget_config_page
from pages.data.transactions.transactions import transactions_page

from pages.reports.current import current_analytics
from pages.reports.monthly import monthly_analytics
from pages.reports.yearly import yearly_analytics
from pages.reports.historical import historical_analytics

from pages.welcome import welcome_page
from pages.guide import guide_page

# Set BASE_URL
ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")
if ENVIRONMENT == "production":
    BACKEND_URL = "https://budget-production-99c8.up.railway.app/api"
else:
    BACKEND_URL = "http://backend:8000/api"

st.set_page_config(
    page_title="Budget Management System",
    page_icon="💰",
    layout="wide"
)

# Initialize session state variables and services
if "api_auth" not in st.session_state:
    st.session_state["api_auth"] = {
        "service": None,
        "base_url": BACKEND_URL,
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
        "cache": {},
    }
    st.session_state["api_locations"]["service"] = LocationsAPIService()

if "api_buckets" not in st.session_state:
    st.session_state["api_buckets"] = {
        "service": None,
        "edit_buc_name": None,
        "delete_buc_name": None,
        "cache": {},
    }
    st.session_state["api_buckets"]["service"] = BucketsAPIService()

if "api_categories" not in st.session_state:
    st.session_state["api_categories"] = {
        "service": None,
        "edit_cat_name": None,
        "delete_cat_name": None,
        "cache": {},
    }
    st.session_state["api_categories"]["service"] = CategoriesAPIService()

if "api_transactions" not in st.session_state:
    st.session_state["api_transactions"] = {
        "service": None,
        "edit_mode": False,
        "delete_mode": False,
        "confirm_delete": False,
        "to_delete": None,
        "to_update": None,
        "new_data": None,
        "filter_mode": False,
        "add_form": False,
        "cache": {},
    }
    st.session_state["api_transactions"]["service"] = TransactionAPIService()

if "api_analytics" not in st.session_state:
    st.session_state["api_analytics"] = {
        "service": None,
        "cache": {},
    }
    st.session_state["api_analytics"]["service"] = AnalyticsAPIService()

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "welcome"

# Define pages
welcome = st.Page(welcome_page, title="Welcome", icon="👋")

login = st.Page(login_page, title="Login", icon="🔑")
signup = st.Page(signup_page, title="Sign Up", icon="✍️")

guide = st.Page(guide_page, title="User Guide", icon="📖")

transactions = st.Page(transactions_page, title="Transaction Management", icon="💸")
budget_settings = st.Page(budget_config_page, title="Budget Configuration", icon="⚙️")

current_status = st.Page(current_analytics, title="Money Distribution", icon="💰")
monthly_report = st.Page(monthly_analytics, title="Monthly report", icon="📅")
yearly_report = st.Page(yearly_analytics, title="Yearly report", icon="🗓️")
historical_report = st.Page(historical_analytics, title="Historical report", icon="📊")

account_settings = st.Page(account_settings_page, title="Edit Account", icon="👤")
signout = st.Page(signout_page, title="Sign Out", icon="🚪")

# Navigation logic
if st.session_state["api_auth"]["authenticated"]:
    pg = st.navigation({
        "Guide": [guide],
        "Data management": [transactions, budget_settings],
        "Reports & Analytics": [current_status, monthly_report, yearly_report, historical_report],
        "Account settings": [account_settings, signout],
    })
else:
    if st.session_state["current_page"] == "signup":
        pg = st.navigation([signup])
    elif st.session_state["current_page"] == "login":
        pg = st.navigation([login])
    else:
        pg = st.navigation([welcome])

# Enjoy!
pg.run()
