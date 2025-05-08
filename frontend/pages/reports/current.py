import time
import matplotlib.pyplot as plt
import random
import altair as alt
import streamlit as st
import pandas as pd

def current_report():
    """Current report section."""

    st.title("📊 Current status report")
    st.write("Here you can see the current status of your budget.")

    # Analytics API and unpacking data
    analytics_api = st.session_state["api_analytics"]["service"]
    data = analytics_api.get_current_analytics()

    locations_data = data["locations"]
    locations_df = pd.DataFrame.from_dict(data["locations"], orient="index", columns=["Amount"])
    locations_df.index.name = "Location"
    only_locations_df = pd.DataFrame.from_dict({k: v for k, v in locations_data.items() if k != "_total"}, orient="index", columns=["Amount"])
    only_locations_df = only_locations_df.reset_index()
    only_locations_df.columns = ["Location", "Amount"]
    locations_total = locations_data["_total"]
    
    buckets_data = data["buckets"]
    buckets_df = pd.DataFrame.from_dict(data["buckets"], orient="index", columns=["Amount"])
    buckets_df.index.name = "Bucket"
    only_buckets_df = pd.DataFrame.from_dict({k: v for k, v in buckets_data.items() if k != "_total"}, orient="index", columns=["Amount"])
    only_buckets_df = only_buckets_df.reset_index()
    only_buckets_df.columns = ["Bucket", "Amount"]
    buckets_total = buckets_data["_total"]
    
    balance_data = {
        "Income": data["balance"]["positive"],
        "Expense": data["balance"]["negative"],
        "neutral": data["balance"]["neutral"],
        "balance": data["balance"]["_total"]
    }
    balance_df = pd.DataFrame.from_dict(balance_data, orient="index", columns=["Amount"])
    balance_df.index.name = "Balance"
    only_balance_df = pd.DataFrame.from_dict({k: v for k, v in balance_data.items() if k != "_total"}, orient="index", columns=["Amount"])
    only_balance_df = only_balance_df.reset_index()
    only_balance_df.columns = ["Balance", "Amount"]
    balance_total = balance_data["_total"]

    # TOTAL
    if locations_total == buckets_total == balance_total:
        st.subheader(f"💰 Money available: {locations_total}")
    else:
        st.warning("The total amounts do not match. Please check your data.")
        st.stop()
    st.markdown("---")
    
    # LOCATIONS SECTION
    st.subheader(f"🏦 Locations ({locations_total})")
    graph, table = st.columns([8, 2])
    
    locations_chart = alt.Chart(locations_df.reset_index()).mark_bar().encode(
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
    
    table.dataframe(only_locations_df.set_index("Location"))
    graph.altair_chart(locations_chart, use_container_width=True)

    # BUCKETS SECTION
    st.subheader(f"🪙 Buckets ({buckets_total})")
    graph, table = st.columns([8, 2])

    buckets_chart = alt.Chart(buckets_df.reset_index()).mark_bar().encode(
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
    
    table.dataframe(only_buckets_df.set_index("Bucket"))
    graph.altair_chart(buckets_chart, use_container_width=True)

    # BALANCE SECTION
    st.subheader(f"⚖️ Balance ({balance_total})")
    graph, table = st.columns([8, 2])

    color_scale = alt.Scale(
        domain=["Income", "Expense"],
        range=["#4CAF50", "#FF7F7F"]
    )

    balance_chart = alt.Chart(balance_df.reset_index()).mark_bar().encode(
        x=alt.X("Balance:N", title=None, sort=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Amount:Q", title=None),
        color=alt.Color("Balance:N", legend=None, scale=color_scale),
        tooltip=["Balance", "Amount"]
    ).configure_axis(
        labelFontSize=16,
        titleFontSize=16
    ).configure_title(
        fontSize=25
    ).transform_filter(
        alt.datum.Balance != "balance"
    )
    
    table.dataframe(only_balance_df.set_index("Balance"))
    graph.altair_chart(balance_chart, use_container_width=True)
