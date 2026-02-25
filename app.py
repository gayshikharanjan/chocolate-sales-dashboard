import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Chocolate Sales Dashboard",
    page_icon="🍫",
    layout="wide"
)

# ===============================
# CUSTOM CSS (Colorful UI)
# ===============================
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to right, #ffecd2, #fcb69f);
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍫 Chocolate Sales Dashboard")
st.markdown("### 📊 Interactive & Creative Data Analysis")

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("Chocolatesales.csv")

df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# 🔥 CLEAN Amount column
df['Amount'] = df['Amount'].replace('[\$,]', '', regex=True).astype(float)

# ===============================
# SIDEBAR FILTER
# ===============================
st.sidebar.header("🔎 Filter Options")

selected_country = st.sidebar.multiselect(
    "Select Country",
    options=df['Country'].unique(),
    default=df['Country'].unique()
)

filtered_df = df[df['Country'].isin(selected_country)]

# ===============================
# KPI METRICS
# ===============================
total_sales = filtered_df['Amount'].sum()
total_boxes = filtered_df['Boxes Shipped'].sum()
total_transactions = len(filtered_df)

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📦 Boxes Shipped", f"{total_boxes:,}")
col3.metric("🧾 Transactions", total_transactions)

st.markdown("---")

# ===============================
# BAR CHART
# ===============================
st.subheader("🌍 Total Sales by Country")

sales_country = filtered_df.groupby('Country')['Amount'].sum().reset_index()

fig1 = px.bar(
    sales_country,
    x="Country",
    y="Amount",
    color="Country",
    template="plotly_dark"
)

st.plotly_chart(fig1, use_container_width=True)

# ===============================
# PIE CHART
# ===============================
st.subheader("🍬 Sales Distribution by Product")

sales_product = filtered_df.groupby('Product')['Amount'].sum().reset_index()

fig2 = px.pie(
    sales_product,
    names="Product",
    values="Amount",
    color_discrete_sequence=px.colors.sequential.Rainbow
)

st.plotly_chart(fig2, use_container_width=True)

# ===============================
# HISTOGRAM
# ===============================
st.subheader("📊 Sales Amount Distribution")

fig3 = px.histogram(
    filtered_df,
    x="Amount",
    nbins=15,
    color_discrete_sequence=["#ff4b4b"]
)

st.plotly_chart(fig3, use_container_width=True)

# ===============================
# SCATTER PLOT
# ===============================
st.subheader("📦 Boxes Shipped vs Sales Amount")

fig4 = px.scatter(
    filtered_df,
    x="Boxes Shipped",
    y="Amount",
    color="Country",
    size="Amount",
    template="plotly_white"
)

st.plotly_chart(fig4, use_container_width=True)

# ===============================
# LINE CHART
# ===============================
st.subheader("📈 Sales Trend Over Time")

sales_time = filtered_df.groupby('Date')['Amount'].sum().reset_index()

fig5 = px.line(
    sales_time,
    x="Date",
    y="Amount",
    markers=True,
    color_discrete_sequence=["#6a11cb"]
)

st.plotly_chart(fig5, use_container_width=True)

st.success("🚀 EDA Completed Successfully!")