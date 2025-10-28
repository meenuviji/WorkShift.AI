import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Workshift.AI Dashboard",
    page_icon="🧠",
    layout="wide"
)

# Load your data
@st.cache_data
def load_data():
    # Replace this with your real CSV or DB call
    return pd.read_csv("workshift_jobs.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Job Listings")
locations = st.sidebar.multiselect("Select Location", df["location"].unique())
skills = st.sidebar.multiselect("Select Required Skills", df["skills_required"].unique())

filtered_df = df.copy()

if locations:
    filtered_df = filtered_df[filtered_df["location"].isin(locations)]
if skills:
    filtered_df = filtered_df[filtered_df["skills_required"].isin(skills)]

# Main dashboard
st.title("📊 Workshift.AI - Tech Job Demand & Automation Risk")

col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", len(filtered_df))
col2.metric("Avg Automation Risk", f"{filtered_df['automation_risk_score'].mean():.2f}")
col3.metric("Avg Salary", f"${filtered_df['salary_estimate'].mean():,.0f}")

st.markdown("### 🔥 Job Titles by Demand")
job_counts = filtered_df["job_title"].value_counts().reset_index()
job_counts.columns = ["job_title", "count"]
fig_demand = px.bar(job_counts.head(10), x="count", y="job_title", orientation="h", title="Top 10 In-Demand Roles")
st.plotly_chart(fig_demand, use_container_width=True)

st.markdown("### 🤖 Automation Risk Distribution")
fig_risk = px.histogram(filtered_df, x="automation_risk_score", nbins=20, title="Automation Risk Score Distribution")
st.plotly_chart(fig_risk, use_container_width=True)

st.markdown("### 📋 Job Listings")
st.dataframe(filtered_df[["job_title", "company", "location", "salary_estimate", "automation_risk_score", "skills_required", "posted_date"]].reset_index(drop=True))

