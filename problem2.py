import streamlit as st
import pandas as pd
#import plotly.graph_objects as go
#import plotly.express as px
import plotly as px


# Load data
@st.cache
def load_data():
    df = pd.read_csv("university_student_dashboard_data.csv")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_term = st.sidebar.selectbox("Select Term", df["Term"].unique())
selected_year = st.sidebar.slider("Select Year", int(df["Year"].min()), int(df["Year"].max()), int(df["Year"].max()))

# Filtering data
filtered_df = df[(df["Term"] == selected_term) & (df["Year"] == selected_year)]

# Main dashboard
st.title("University Admissions & Student Satisfaction Dashboard")

# Applications, Admissions & Enrollment
st.subheader("Applications, Admissions & Enrollments")
col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", filtered_df["Applications"].sum())
col2.metric("Total Admissions", filtered_df["Admissions"].sum())
col3.metric("Total Enrollments", filtered_df["Enrollments"].sum())

# Retention Rate Trend
st.subheader("Retention Rate Over Time")
retention_trend = df.groupby("Year")["Retention Rate"].mean().reset_index()
fig_retention = px.line(retention_trend, x="Year", y="Retention Rate", markers=True, title="Retention Rate Trend")
st.plotly_chart(fig_retention)

# Student Satisfaction Trend
st.subheader("Student Satisfaction Over Years")
satisfaction_trend = df.groupby("Year")["Satisfaction Score"].mean().reset_index()
fig_satisfaction = px.line(satisfaction_trend, x="Year", y="Satisfaction Score", markers=True, title="Satisfaction Score Trend")
st.plotly_chart(fig_satisfaction)

# Enrollment Breakdown by Department
st.subheader("Enrollment Breakdown by Department")
enrollment_by_dept = filtered_df.groupby("Department")["Enrollments"].sum().reset_index()
fig_dept = px.bar(enrollment_by_dept, x="Department", y="Enrollments", title="Enrollment by Department")
st.plotly_chart(fig_dept)

# Spring vs Fall Trends
st.subheader("Spring vs. Fall Term Comparison")
term_comparison = df.groupby(["Term", "Year"])[["Enrollments", "Retention Rate", "Satisfaction Score"]].mean().reset_index()
fig_term = px.line(term_comparison, x="Year", y=["Enrollments", "Retention Rate", "Satisfaction Score"], color="Term", markers=True, title="Spring vs Fall Trends")
st.plotly_chart(fig_term)



