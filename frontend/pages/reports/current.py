import altair as alt
import streamlit as st
import pandas as pd

def process_current_status_data():
    """Prepare data for charts."""

    # Analytics API and unpacking data
    analytics_api = st.session_state["api_analytics"]["service"]
    data = analytics_api.get_current_analytics()

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

    st.title("📊 Current status report")
    st.write("Here you can see the current status of your budget.")

    # Analytics API and unpacking data
    processed_data = process_current_status_data()
    
    locations_chart = processed_data["locations"]["for_chart"]
    locations_table = processed_data["locations"]["for_table"]
    locations_total = processed_data["locations"]["total"]
    
    buckets_chart = processed_data["buckets"]["for_chart"]
    buckets_table = processed_data["buckets"]["for_table"]
    buckets_total = processed_data["buckets"]["total"]
    
    balance_chart = processed_data["balance"]["for_chart"]
    balance_table = processed_data["balance"]["for_table"]
    balance_total = processed_data["balance"]["total"]


    # CHECKINT TOTALS MATCHING
    if locations_total == buckets_total == balance_total:
        st.subheader(f"💰 Money available: {locations_total}")
    else:
        st.warning("The total amounts do not match. Please check your data.")
        st.stop()
    st.markdown("---")
    
    # LOCATIONS SECTION
    st.subheader(f"🏦 Locations ({locations_total})")
    graph, table = st.columns([8, 2])
    
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
    table.dataframe(locations_table)
    graph.altair_chart(locations_chart, use_container_width=True)

    # BUCKETS SECTION
    st.subheader(f"🪙 Buckets ({buckets_total})")
    graph, table = st.columns([8, 2])

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
    table.dataframe(buckets_table)
    graph.altair_chart(buckets_chart, use_container_width=True)

    # BALANCE SECTION
    st.subheader(f"⚖️ Balance ({balance_total})")
    graph, table = st.columns([8, 2])

    color_scale = alt.Scale(
        domain=["Positive", "Negative", "Neutral"],
        range=["#4CAF50", "#FF7F7F", "#898989"]
    )

    balance_chart = alt.Chart(balance_chart.reset_index()).mark_bar().encode(
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
        alt.datum.Balance != "_total"
    )
    
    balance_table = balance_table.set_index("Balance")
    table.dataframe(balance_table)
    graph.altair_chart(balance_chart, use_container_width=True)

    st.info("POSITIVE: money coming in (e.g. Income). NEGATIVE: money going out (e.g. Expense). NEUTRAL: moving between locations/buckets or temporary transactions (e.g. Transfer, Loans).")
