import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="🍫 Chocolate Sales Dashboard",
    page_icon="🍫",
    layout="wide"
)

st.title("🍫 Chocolate Sales Dashboard")
st.markdown("### Interactive & Creative Sales Analysis")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Chocolatesales.csv")

    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

    # Clean Amount column if it contains $
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
# KPI METRICS
# -----------------------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"${filtered_df['Amount'].sum():,.0f}")
col2.metric("📦 Total Boxes", f"{filtered_df['Boxes Shipped'].sum():,}")
col3.metric("🌍 Total Countries", filtered_df['Country'].nunique())

st.divider()

# -----------------------------
# BAR CHART - SALES BY COUNTRY
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
# PIE CHART - PRODUCT DISTRIBUTION
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
# LINE CHART - SALES TREND
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

# -----------------------------
# HISTOGRAM - SALES DISTRIBUTION
# -----------------------------
fig_hist = px.histogram(
    filtered_df,
    x="Amount",
    nbins=20,
    title="📊 Sales Amount Distribution",
    template="plotly_dark"
)

# -----------------------------
# SCATTER - BOXES VS AMOUNT
# -----------------------------
fig_scatter = px.scatter(
    filtered_df,
    x="Boxes Shipped",
    y="Amount",
    color="Country",
    size="Amount",
    hover_data=["Product"],
    title="📦 Boxes Shipped vs Sales Amount",
    template="plotly_dark"
)

col4, col5 = st.columns(2)

with col4:
    st.plotly_chart(fig_hist, use_container_width=True)

with col5:
    st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------
# MONTHLY SALES TREND
# -----------------------------
filtered_df['Month'] = filtered_df['Date'].dt.to_period("M").astype(str)

monthly_sales = filtered_df.groupby("Month")["Amount"].sum().reset_index()

fig_month = px.area(
    monthly_sales,
    x="Month",
    y="Amount",
    title="📅 Monthly Sales Trend",
    template="plotly_dark"
)

st.plotly_chart(fig_month, use_container_width=True)

st.success("✅ Dashboard Loaded Successfully 🚀")