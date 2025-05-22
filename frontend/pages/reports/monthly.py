import altair as alt
import streamlit as st
import pandas as pd
import calendar

def monthly_analytics():
    """Monthly report section."""

    st.title("📅 Monthly report")
    st.write("Here you can see monthly reports.")

    if not st.session_state["api_transactions"]["cache"]["list"]:
        st.warning("No transactions yet. Come back here when you add some transactions.")
        return

    # Analytics API and unpacking data
    analytics_api = st.session_state["api_analytics"]["service"]
    
    years = st.session_state["api_analytics"]["cache"]["years"]
    month_names = list(calendar.month_name)[1:]

    col1, col2 = st.columns(2)
    year = col1.selectbox("Year:", options=years, index=len(years)-1)
    month = col2.selectbox("Month:", options=month_names)
    month_index = month_names.index(month) + 1
    
    data = analytics_api.get_monthly_analytics(year=year, month=month_index)

    positive_categories_df = pd.DataFrame.from_dict(data["positive_categories"], orient="index", columns=["Amount"])
    positive_categories_df.index.name = "Positive Categories"
    positive_categories_total = sum(positive_categories_df["Amount"])
    
    negative_categories_df = pd.DataFrame.from_dict(data["negative_categories"], orient="index", columns=["Amount"])
    negative_categories_df.index.name = "Negative Categories"
    negative_categories_total = sum(negative_categories_df["Amount"])

    neutral_categories_df = pd.DataFrame.from_dict(data["neutral_categories"], orient="index", columns=["Amount"])
    neutral_categories_df.index.name = "Neutral Categories"
    neutral_categories_total = sum(neutral_categories_df["Amount"])
    
    balance_data = {
        "_total": data["balance"]["_total"],
        "Positive": data["balance"]["positive"],
        "Negative": data["balance"]["negative"],
        "Neutral": data["balance"]["neutral"],
    }
    balance_df = pd.DataFrame.from_dict(balance_data, orient="index", columns=["Amount"])
    balance_df.index.name = "Balance"
    only_balance_df = pd.DataFrame.from_dict({k: v for k, v in balance_data.items() if k != "_total"}, orient="index", columns=["Amount"])
    only_balance_df = only_balance_df.reset_index()
    only_balance_df.columns = ["Balance", "Amount"]
    balance_total = balance_data["_total"]

    # BALANCE SECTION
    st.markdown("---")
    st.subheader(f"⚖️ Balance ({balance_total})")
    col1, col2 = st.columns([8, 2])

    color_scale = alt.Scale(
        domain=["Positive", "Negative", "Neutral"],
        range=["#4CAF50", "#FF7F7F", "#898989"]
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
        alt.datum.Balance != "_total"
    )
    
    col1.altair_chart(balance_chart, use_container_width=True)
    col2.dataframe(only_balance_df.set_index("Balance"), use_container_width=True)

    st.info("POSITIVE: money coming in (e.g. Income). NEGATIVE: money going out (e.g. Expense). NEUTRAL: moving between locations/buckets or temporary transactions (e.g. Transfer, Loans).")

    # POSITIVE CATEGORIES SECTION
    st.markdown("---")
    st.subheader(f"🟢 Positive categories ({positive_categories_total:.2f})")
    
    if "POSITIVE" in st.session_state["api_categories"]["cache"]["signs"]:
        col1, col2 = st.columns([8, 2])
        
        positive_categories_chart = alt.Chart(positive_categories_df.reset_index()).mark_bar().encode(
            x=alt.X("Positive Categories:N", title=None, sort=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Amount:Q", title=None),
            color=alt.Color("Positive Categories:N", legend=None),
            tooltip=["Positive Categories", "Amount"]
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=16
        ).configure_title(
            fontSize=25
        )
        
        col1.altair_chart(positive_categories_chart, use_container_width=True)
        col2.dataframe(positive_categories_df, use_container_width=True)
    
    else:
        st.info("There are no positive categories.")

    # NEGATIVE CATEGORIES SECTION
    st.markdown("---")
    st.subheader(f"🔴 Negative categories ({negative_categories_total:.2f})")

    if "NEGATIVE" in st.session_state["api_categories"]["cache"]["signs"]:
        col1, col2 = st.columns([8, 2])
        
        negative_categories_chart = alt.Chart(negative_categories_df.reset_index()).mark_bar().encode(
            x=alt.X("Negative Categories:N", title=None, sort=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Amount:Q", title=None),
            color=alt.Color("Negative Categories:N", legend=None),
            tooltip=["Negative Categories", "Amount"]
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=16
        ).configure_title(
            fontSize=25
        )

        col1.altair_chart(negative_categories_chart, use_container_width=True)
        col2.dataframe(negative_categories_df, use_container_width=True)
    
    else:
        st.info("There are no negative categories.")

    # NEUTRAL CATEGORIES SECTION
    st.markdown("---")
    st.subheader(f"⚪ Neutral categories ({neutral_categories_total:.2f})")
    
    if "NEUTRAL" in st.session_state["api_categories"]["cache"]["signs"]:
        col1, col2 = st.columns([8, 2])
        
        neutral_categories_chart = alt.Chart(neutral_categories_df.reset_index()).mark_bar().encode(
            x=alt.X("Neutral Categories:N", title=None, sort=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Amount:Q", title=None),
            color=alt.Color("Neutral Categories:N", legend=None),
            tooltip=["Neutral Categories", "Amount"]
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=16
        ).configure_title(
            fontSize=25
        )

        col1.altair_chart(neutral_categories_chart, use_container_width=True)
        col2.dataframe(neutral_categories_df, use_container_width=True)

    else:
        st.info("There are no neutral categories.")