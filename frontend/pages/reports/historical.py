import altair as alt
import streamlit as st
import pandas as pd

def build_category_table(yearly_data, category_type):
    all_categories = set()
    
    for year_data in yearly_data.values():
        all_categories.update(year_data.get(category_type, {}).keys())
    
    df = pd.DataFrame(index=sorted(all_categories))
    
    for year, year_data in yearly_data.items():
        values = {}
        
        for category, amount in year_data.get(category_type, {}).items():
            values[category] = amount
        
        df[year] = pd.Series(values)
    
    return df.fillna(0)

def build_category_chart(yearly_data, category_type):
    results = []

    for year, year_data in yearly_data.items():

        balance_data = year_data.get("balance", {})

        if category_type == "balance":
            value = balance_data.get("_total", 0)
        else:
            value = balance_data.get(category_type, 0)

        results.append({
            "Year": year,
            "Total": value
        })

    return pd.DataFrame(results)

def historical_analytics():
    """Yearly report section."""

    st.title("📊 Historical report")
    st.write("Here you can see historical analytics of your budget across all years.")

    if not st.session_state["api_transactions"]["cache"]["list"]:
        st.warning("No transactions yet. Come back here when you add some transactions.")
        return

    # Analytics API and preparing data
    analytics_api = st.session_state["api_analytics"]["service"]
    data = analytics_api.get_historical_analytics()
    
    yearly_data = data["yearly"]

    positive_categories_df = pd.DataFrame.from_dict(data["summary"]["positive_categories"], orient="index", columns=["Amount"])
    positive_categories_df.index.name = "Positive Categories"
    positive_categories_total = sum(positive_categories_df["Amount"])
    
    negative_categories_df = pd.DataFrame.from_dict(data["summary"]["negative_categories"], orient="index", columns=["Amount"])
    negative_categories_df.index.name = "Negative Categories"
    negative_categories_total = sum(negative_categories_df["Amount"])

    neutral_categories_df = pd.DataFrame.from_dict(data["summary"]["neutral_categories"], orient="index", columns=["Amount"])
    neutral_categories_df.index.name = "Neutral Categories"
    neutral_categories_total = sum(neutral_categories_df["Amount"])
    
    balance_data = {
        "_total": data["summary"]["balance"]["_total"],
        "Positive": data["summary"]["balance"]["positive"],
        "Negative": data["summary"]["balance"]["negative"],
        "Neutral": data["summary"]["balance"]["neutral"],
    }
    balance_df = pd.DataFrame.from_dict(balance_data, orient="index", columns=["Amount"])
    balance_df.index.name = "Balance"
    only_balance_df = pd.DataFrame.from_dict({k: v for k, v in balance_data.items() if k != "_total"}, orient="index", columns=["Amount"])
    only_balance_df = only_balance_df.reset_index()
    only_balance_df.columns = ["Balance", "Amount"]
    only_balance_df.index.name = "Balance"
    balance_total = balance_data["_total"]

    # BALANCE DATA
    st.markdown("---")
    st.subheader(f"⚖️ Balance ({balance_total})")

    color_scale = alt.Scale(
        domain=["Positive", "Negative", "Neutral"],
        range=["#4CAF50", "#FF7F7F", "#898989"]
    )

    container = st.container(border=False)
    row1, row2 = container.container(), container.container()
    
    # per category
    col1, col2 = row1.columns([8, 2])

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
    col2.dataframe(only_balance_df, use_container_width=True, hide_index=True)
    
    row1.info("POSITIVE: money coming in (e.g. Income). NEGATIVE: money going out (e.g. Expense). NEUTRAL: moving between locations/buckets or temporary transactions (e.g. Transfer, Loans).")

    # per year
    col1, col2 = row2.columns([8, 2])
    yearly_balance_chart = build_category_chart(yearly_data, "balance")
    balance_chart = alt.Chart(yearly_balance_chart.reset_index()).mark_bar().encode(
        x=alt.X("Year:N", title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Total:Q", title=None),
        color=alt.value("#00A2FF"),
        tooltip=["Year", "Total"]
    ).configure_axis(
        labelFontSize=16,
        titleFontSize=16
    ).configure_title(
        fontSize=25
    )
    col1.altair_chart(balance_chart, use_container_width=True)
    col2.dataframe(yearly_balance_chart.set_index("Year"), use_container_width=True)

    # POSITIVE DATA
    st.markdown("---")
    st.subheader(f"🟢 Positive categories ({positive_categories_total})")
    
    if "POSITIVE" in st.session_state["api_categories"]["cache"]["signs"]:
        container = st.container(border=False)
        row1, row2 = container.container(), container.container()
        
        # per category
        col1, col2 = row1.columns([8, 2])
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
        
        positive_categories_table = build_category_table(yearly_data, "positive_categories")
        st.dataframe(positive_categories_table, use_container_width=True)
        
        # per year
        col1, col2 = row2.columns([8, 2])
        positive_data = build_category_chart(yearly_data, "positive")
        positive_chart = alt.Chart(positive_data.reset_index()).mark_bar().encode(
            x=alt.X("Year:N", title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Total:Q", title=None),
            color=alt.value("#4CAF50"),
            tooltip=["Year", "Total"]
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=16
        ).configure_title(
            fontSize=25
        )
        col1.altair_chart(positive_chart, use_container_width=True)
        col2.dataframe(positive_data.set_index("Year"), use_container_width=True)
    
    else:
        st.info("There are no positive categories.")

    # NEGATIVE DATA
    st.markdown("---")
    st.subheader(f"🔴 Negative categories ({negative_categories_total})")

    if "NEGATIVE" in st.session_state["api_categories"]["cache"]["signs"]:
        container = st.container(border=False)
        row1, row2 = container.container(), container.container()

        # per category
        col1, col2 = row1.columns([8, 2])
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
        
        negative_categories_table = build_category_table(yearly_data, "negative_categories")
        st.dataframe(negative_categories_table, use_container_width=True)

        # per year
        col1, col2 = row2.columns([8, 2])
        yearly_negative_chart = build_category_chart(yearly_data, "negative")
        negative_chart = alt.Chart(yearly_negative_chart.reset_index()).mark_bar().encode(
            x=alt.X("Year:N", title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Total:Q", title=None),
            color=alt.value("#FF7F7F"),
            tooltip=["Year", "Total"]
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=16
        ).configure_title(
            fontSize=25
        )
        col1.altair_chart(negative_chart, use_container_width=True)
        col2.dataframe(yearly_negative_chart.set_index("Year"), use_container_width=True)

    else:
        st.info("There are no negative categories.")

    # NEUTRAL DATA
    st.markdown("---")
    st.subheader(f"⚪ Neutral categories ({neutral_categories_total})")

    if "NEUTRAL" in st.session_state["api_categories"]["cache"]["signs"]:
        container = st.container(border=False)
        row1, row2 = container.container(), container.container()

        # per category
        col1, col2 = row1.columns([8, 2])
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
        
        neutral_categories_table = build_category_table(yearly_data, "neutral_categories")
        st.dataframe(neutral_categories_table, use_container_width=True)

    else:
        st.info("There are no neutral categories.")