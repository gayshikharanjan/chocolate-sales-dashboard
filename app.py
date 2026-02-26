import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="🍫 Chocolate Sales Dashboard",
                   page_icon="🍫",
                   layout="wide")

st.title("🍫 Chocolate Sales Dashboard")
st.markdown("### Interactive & Creative Sales Analysis")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Chocolatesales.csv")   # Make sure name matches exactly
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

    # Clean Amount column if it has $
    df['Amount'] = (
        df['Amount']
        .replace('[\$,]', '', regex=True)
        .astype(float)
    )
    return df

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔎 Filter Data")

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=df['Country'].unique(),
    default=df['Country'].unique()
)

product_filter = st.sidebar.multiselect(
    "Select Product",
    options=df['Product'].unique(),
    default=df['Product'].unique()
)

filtered_df = df[
    (df['Country'].isin(country_filter)) &
    (df['Product'].isin(product_filter))
]

# -----------------------------
# KPI SECTION
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"${filtered_df['Amount'].sum():,.0f}")
col2.metric("📦 Total Boxes", f"{filtered_df['Boxes Shipped'].sum():,}")
col3.metric("🌍 Countries", filtered_df['Country'].nunique())

st.divider()

# -----------------------------
# BAR CHART
# -----------------------------
sales_country = filtered_df.groupby("Country")["Amount"].sum().reset_index()

fig_bar = px.bar(
    sales_country,
    x="Country",
    y="Amount",
    color="Country",
    title="🌍 Total Sales by Country",
    template="plotly_dark"
)

st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------
# PIE CHART
# -----------------------------
sales_product = filtered_df.groupby("Product")["Amount"].sum().reset_index()

fig_pie = px.pie(
    sales_product,
    names="Product",
    values="Amount",
    title="🍫 Sales Distribution by Product",
    hole=0.4
)

st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------
# LINE CHART
# -----------------------------
sales_time = filtered_df.groupby("Date")["Amount"].sum().reset_index()

fig_line = px.line(
    sales_time,
    x="Date",
    y="Amount",
    title="📈 Sales Trend Over Time",
    markers=True
)

st.plotly_chart(fig_line, use_container_width=True)

st.success("✅ Dashboard Loaded Successfully!")