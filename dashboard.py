import os; os.system("pip install pandas plotly scipy")
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration Setup
st.set_page_config(page_title="Retail Sales KPI Dashboard", layout="wide")
st.title("📊 Executive KPI & Interactive Sales Dashboard")

# 2. Load Your Live Data File
filename = 'retail_sales.csv.csv'
try:
    df = pd.read_csv(filename)
except FileNotFoundError:
    st.error(f"Missing file: {filename}")
    st.stop()

# 3. Interactive Sidebar Filters
st.sidebar.header("Dashboard Parameters")
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

if not numeric_cols:
    st.error("No numeric columns found to calculate KPIs.")
    st.stop()

# Choose target column dynamically
target_metric = st.sidebar.selectbox("Select Core Target Metric:", numeric_cols)

# 4. Interactive KPI Scorecard Metrics
st.subheader("Key Performance Indicators (KPIs)")
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric(label="Total Transactional Records", value=f"{len(df):,}")
with metric_col2:
    st.metric(label=f"Average {target_metric}", value=f"{df[target_metric].mean():,.2f}")
with metric_col3:
    st.metric(label=f"Maximum Record Value", value=f"{df[target_metric].max():,}")

st.markdown("---")

# 5. Interactive Plotly Charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Distribution Over Density")
    fig_hist = px.histogram(df, x=target_metric, marginal="box", color_discrete_sequence=['#4361ee'])
    st.plotly_chart(fig_hist, use_container_width=True)

with chart_col2:
    st.subheader("Multi-Variable Comparative Data Split")
    if len(numeric_cols) > 1:
        second_metric = st.selectbox("Select Comparative Variable:", numeric_cols, index=1 if len(numeric_cols)>1 else 0)
        fig_scatter = px.scatter(df, x=second_metric, y=target_metric, trendline="ols", color_discrete_sequence=['#f72585'])
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Add more numerical columns to view multi-variable tracking.")
