import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Chocolate Sales Dashboard",
    page_icon="🍫",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = pd.read_csv("DATASETT/Chocolatesales.csv")
df.columns = df.columns.str.strip()

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("🔎 Filters")

# Product Filter
product_filter = st.sidebar.multiselect(
    "Select Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

# Country Filter
country_filter = st.sidebar.multiselect(
    "Select Country",
    options=df["Country"].unique(),
    default=df["Country"].unique()
)

# Date Filter
if "Date" in df.columns:
    date_filter = st.sidebar.date_input(
        "Select Date Range",
        [df["Date"].min(), df["Date"].max()]
    )

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------
filtered_df = df[
    (df["Product"].isin(product_filter)) &
    (df["Country"].isin(country_filter))
]

if "Date" in df.columns:
    filtered_df = filtered_df[
        (filtered_df["Date"] >= pd.to_datetime(date_filter[0])) &
        (filtered_df["Date"] <= pd.to_datetime(date_filter[1]))
    ]

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("🍫 Chocolate Sales Dashboard")
st.markdown("---")

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------
total_revenue = filtered_df["Revenue"].sum()
total_units = filtered_df["Units Sold"].sum()
avg_revenue = filtered_df["Revenue"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
col2.metric("Total Units Sold", f"{total_units:,.0f}")
col3.metric("Average Revenue", f"₹ {avg_revenue:,.0f}")

st.markdown("---")

# --------------------------------------------------
# CHART 1 - Revenue by Product
# --------------------------------------------------
st.subheader("Revenue by Product")

product_chart = px.bar(
    filtered_df,
    x="Product",
    y="Revenue",
    color="Product",
)

st.plotly_chart(product_chart, use_container_width=True)

# --------------------------------------------------
# CHART 2 - Revenue by Country
# --------------------------------------------------
st.subheader("Revenue by Country")

country_chart = px.pie(
    filtered_df,
    names="Country",
    values="Revenue",
)

st.plotly_chart(country_chart, use_container_width=True)

# --------------------------------------------------
# CHART 3 - Sales Trend
# --------------------------------------------------
if "Date" in df.columns:
    st.subheader("Revenue Trend Over Time")

    trend_data = filtered_df.groupby("Date")["Revenue"].sum().reset_index()

    trend_chart = px.line(
        trend_data,
        x="Date",
        y="Revenue",
    )

    st.plotly_chart(trend_chart, use_container_width=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.caption("Built with Streamlit 🚀 | Corporate Sales Dashboard")
import os
st.write(os.listdir())