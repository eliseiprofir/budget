import altair as alt
import streamlit as st
import pandas as pd

from utils.cache_utils import cache_fetched

from utils.cache_utils import get_or_fetch_transactions_page

from utils.cache_utils import get_or_fetch_current_analytics


def process_current_status_data():
    """Prepare data for charts."""

    data = get_or_fetch_current_analytics()

    locations_data = data["locations"]
    locations_df = pd.DataFrame.from_dict(data["locations"], orient="index", columns=["Amount"])
    locations_df.index.name = "Location"
    locations_table = pd.DataFrame.from_dict({k: v for k, v in locations_data.items() if k != "_total"}, orient="index", columns=["Amount"])
    locations_table = locations_table.reset_index()
    locations_table.columns = ["Location", "Amount"]
    locations_total = locations_data["_total"]
    
    buckets_data = data["buckets"]
    buckets_df = pd.DataFrame.from_dict(data["buckets"], orient="index", columns=["Amount"])
    buckets_df.index.name = "Bucket"
    buckets_table = pd.DataFrame.from_dict({k: v for k, v in buckets_data.items() if k != "_total"}, orient="index", columns=["Amount"])
    buckets_table = buckets_table.reset_index()
    buckets_table.columns = ["Bucket", "Amount"]
    buckets_total = buckets_data["_total"]
    
    balance_data = {
        "_total": data["balance"]["_total"],
        "Positive": data["balance"]["positive"],
        "Negative": data["balance"]["negative"],
        "Neutral": data["balance"]["neutral"],
    }
    balance_df = pd.DataFrame.from_dict(balance_data, orient="index", columns=["Amount"])
    balance_df.index.name = "Balance"
    balance_table = pd.DataFrame.from_dict({k: v for k, v in balance_data.items() if k != "_total"}, orient="index", columns=["Amount"])
    balance_table = balance_table.reset_index()
    balance_table.columns = ["Balance", "Amount"]
    balance_total = balance_data["_total"]

    return {
        "locations": {
            "for_chart": locations_df,
            "for_table": locations_table,
            "total": locations_total,
        },
        "buckets": {
            "for_chart": buckets_df,
            "for_table": buckets_table,
            "total": buckets_total,
        },
        "balance": {
            "for_chart": balance_df,
            "for_table": balance_table,
            "total": balance_total,
        }
    }

def current_analytics():
    """Current report section."""

    st.title("💰 Money distribution")
    st.write("Here you can see the current distribution of your available money across different locations and buckets.")
    
    if not cache_fetched(["transactions", "current_analytics"]):
        with st.spinner("Loading data..."):
            get_or_fetch_transactions_page()
            get_or_fetch_current_analytics()

    if not st.session_state["api_transactions"]["cache"]["info"]["has_transactions"]:
        st.warning("No transactions yet. Come back here when you add some transactions.")
        return
    
    # Analytics API and unpacking data
    processed_data = process_current_status_data()
    
    locations_chart = processed_data["locations"]["for_chart"]
    locations_table = processed_data["locations"]["for_table"]
    locations_total = processed_data["locations"]["total"]
    
    buckets_chart = processed_data["buckets"]["for_chart"]
    buckets_table = processed_data["buckets"]["for_table"]
    buckets_total = processed_data["buckets"]["total"]
    
    # LOCATIONS SECTION
    st.subheader(f"🏦 Locations ({locations_total:.2f})")
    col1, col2 = st.columns([8, 2])
    
    locations_chart = alt.Chart(locations_chart.reset_index()).mark_bar().encode(
        x=alt.X("Location:N", title=None, sort=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Amount:Q", title=None),
        color=alt.Color("Location:N", legend=None),
        tooltip=["Location", "Amount"]
    ).configure_axis(
        labelFontSize=16,
        titleFontSize=16
    ).configure_title(
        fontSize=25
    ).transform_filter(
        alt.datum.Location != "_total"
    )
    
    locations_table = locations_table.set_index("Location")
    col1.altair_chart(locations_chart, use_container_width=True)
    col2.dataframe(locations_table, use_container_width=True)

    # BUCKETS SECTION
    st.subheader(f"🪙 Buckets ({buckets_total:.2f})")
    col1, col2 = st.columns([8, 2])

    buckets_chart = alt.Chart(buckets_chart.reset_index()).mark_bar().encode(
        x=alt.X("Bucket:N", title=None, sort=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Amount:Q", title=None),
        color=alt.Color("Bucket:N", legend=None),
        tooltip=["Bucket", "Amount"]
    ).configure_axis(
        labelFontSize=16,
        titleFontSize=16
    ).configure_title(
        fontSize=25
    ).transform_filter(
        alt.datum.Bucket != "_total"
    )
    
    buckets_table = buckets_table.set_index("Bucket")
    col1.altair_chart(buckets_chart, use_container_width=True)
    col2.dataframe(buckets_table, use_container_width=True)
