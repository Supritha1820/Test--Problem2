import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("university_student_dashboard_data.csv")

st.write("Columns in CSV:", df.columns.tolist())


# Strip spaces from column names
df.columns = df.columns.str.strip()

# Convert "Year" to string to avoid issues with categorical plotting
df["Year"] = df["Year"].astype(str)

# Sidebar filters
st.sidebar.header("Filter Options")
selected_years = st.sidebar.multiselect("Select Year", df["Year"].unique(), default=df["Year"].unique())
selected_terms = st.sidebar.multiselect("Select Term", df["Term"].unique(), default=df["Term"].unique())

# Filter data based on user selection
filtered_df = df[(df["Year"].isin(selected_years)) & (df["Term"].isin(selected_terms))]

# Dashboard Title
st.title("🎓 University Admissions & Student Satisfaction Dashboard")

# Key Metrics
st.subheader("Applications, Admissions & Enrollments")
col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", filtered_df["Applications"].sum())
col2.metric("Total Admitted", filtered_df["Admitted"].sum())  # Fixed column name
col3.metric("Total Enrolled", filtered_df["Enrolled"].sum())

# Retention Rate Trend
st.subheader("📊 Retention Rate Over the Years")
fig_retention = px.line(
    df,
    x="Year",
    y="Retention Rate (%)",
    color="Term",
    markers=True,
    title="Retention Rate Trend"
)
st.plotly_chart(fig_retention)

# Student Satisfaction Trend
st.subheader("😊 Student Satisfaction Over the Years")
fig_satisfaction = px.line(
    df,
    x="Year",
    y="Student Satisfaction (%)",
    color="Term",
    markers=True,
    title="Student Satisfaction Trend"
)
st.plotly_chart(fig_satisfaction)

# Enrollment Breakdown by Department
st.subheader("📚 Enrollment Breakdown by Department")
dept_columns = ["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]
df_dept = filtered_df.melt(id_vars=["Year", "Term"], value_vars=dept_columns, var_name="Department", value_name="Enrollment")

fig_dept = px.bar(
    df_dept,
    x="Year",
    y="Enrollment",
    color="Department",
    barmode="group",
    title="Enrollment by Department"
)
st.plotly_chart(fig_dept)

# Spring vs. Fall Comparison
st.subheader("🌱 Spring vs. 🍂 Fall Enrollment Trends")
fig_term_comparison = px.bar(
    df,
    x="Year",
    y="Enrolled",
    color="Term",
    barmode="group",
    title="Enrollment Comparison: Spring vs. Fall"
)
st.plotly_chart(fig_term_comparison)

# Insights
st.subheader("🔍 Key Insights & Recommendations")
st.write("""
- The retention rate has **increased/decreased** over the years. Consider implementing student engagement programs.
- Student satisfaction is **trending upwards/downwards**, possibly indicating areas for improvement.
- Enrollment in **Engineering/Business/Arts/Science** is experiencing growth/decline, suggesting shifts in student interest.
- Spring vs. Fall trends show **higher/lower** enrollment in certain terms. Consider optimizing admission strategies.
""")


