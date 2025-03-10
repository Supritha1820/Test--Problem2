import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("university_student_dashboard_data.csv")

st.write("Columns in CSV:", df.columns.tolist())

# Rename columns for consistency
df.columns = df.columns.str.strip()  # Remove any extra spaces

# Convert Year column to string for plotting
df["Year"] = df["Year"].astype(str)

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_years = st.sidebar.multiselect("Select Year", df["Year"].unique(), default=df["Year"].unique())
selected_terms = st.sidebar.multiselect("Select Term", df["Term"].unique(), default=df["Term"].unique())

# Filter data based on selections
filtered_df = df[(df["Year"].isin(selected_years)) & (df["Term"].isin(selected_terms))]

# Title of Dashboard
st.title("📊 University Student Dashboard")
st.markdown("### Track Admissions, Retention, and Satisfaction Trends Over Time")

# ---- KEY METRICS ----
st.subheader("📌 Applications, Admissions & Enrollments")
col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", filtered_df["Applications"].sum())
col2.metric("Total Admissions", filtered_df["Admitted"].sum())
col3.metric("Total Enrollments", filtered_df["Enrolled"].sum())

# ---- RETENTION RATE TREND ----
st.subheader("📈 Retention Rate Over Time")
fig_retention = px.line(filtered_df, x="Year", y="Retention Rate (%)", markers=True, 
                        title="Retention Rate Trend Over the Years")
st.plotly_chart(fig_retention)

# ---- STUDENT SATISFACTION ----
st.subheader("😊 Student Satisfaction Over Time")
fig_satisfaction = px.line(filtered_df, x="Year", y="Student Satisfaction (%)", markers=True, 
                           title="Student Satisfaction Trend Over the Years")
st.plotly_chart(fig_satisfaction)

# ---- DEPARTMENTAL ENROLLMENT TRENDS ----
st.subheader("📚 Enrollment Breakdown by Department")

dept_columns = ["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]
df_dept = filtered_df.melt(id_vars=["Year"], value_vars=dept_columns, 
                           var_name="Department", value_name="Enrollment")

fig_dept = px.line(df_dept, x="Year", y="Enrollment", color="Department", markers=True, 
                   title="Departmental Enrollment Trends")
st.plotly_chart(fig_dept)

# ---- Spring vs. Fall Enrollment Comparison ----
st.subheader("🌱 Spring vs. 🍂 Fall Enrollment Trends")
fig_term_comparison = px.bar(df, x="Year", y="Enrolled", color="Term", barmode="group", title="Enrollment: Spring vs. Fall")
st.plotly_chart(fig_term_comparison)

# ---- RETENTION VS. SATISFACTION ----
st.subheader("📊 Retention Rate vs. Student Satisfaction")
fig_compare = px.scatter(filtered_df, x="Retention Rate (%)", y="Student Satisfaction (%)", 
                         color="Year", size="Enrolled", 
                         title="Correlation Between Retention and Satisfaction")
st.plotly_chart(fig_compare)

# ---- TERM COMPARISON (Spring vs. Fall) ----
st.subheader("📅 Enrollment by Term")
fig_term_comparison = px.bar(filtered_df, x="Year", y="Enrolled", color="Term", 
                             barmode="group", title="Spring vs. Fall Enrollment Trends")
st.plotly_chart(fig_term_comparison)

# ---- MULTI-TREND COMPARISON (Retention, Satisfaction, Enrollments) ----
st.subheader("📊 Trends: Retention Rate, Satisfaction, and Enrollments")
fig_trend = px.line(filtered_df, x="Year", y=["Retention Rate (%)", "Student Satisfaction (%)", "Enrolled"], 
                     markers=True, title="Comparing Retention, Satisfaction, and Enrollments",
                     labels={"value": "Percentage / Enrollment", "variable": "Metric"})
st.plotly_chart(fig_trend)

# ---- INSIGHTS & RECOMMENDATIONS ----
st.subheader("🔍 Key Insights & Recommendations")
st.write("""
-  **Applications, Admissions, & Enrollments:** 
    The conversion rate from applications → admitted → enrolled students can indicate the selectivity and attractiveness of the university.
   
    If applications increase but enrollments decline, it might indicate admissions policies need review, or students are choosing other universities.
- **Retention Rate Trends Over Time:**
    If retention rates are increasing, it suggests improved student support and engagement.
    
    If retention rates drop in specific years, it could indicate academic difficulty, dissatisfaction, or external factors (e.g., pandemic impact).
- **Student Satisfaction Over Time:**
    A steady or increasing satisfaction level means students are happy with academics, facilities, and campus life.
   
    A drop in satisfaction might indicate problems like overcrowded classes, faculty issues, or poor student services.
- **Enrollment Breakdown by Department:**
    Engineering and Business enrollments may be growing, indicating higher demand for these fields.
    
    If Arts and Science enrollments are declining, it could signal lower student interest or fewer job opportunities.
- **Enrollment Comparison: Spring vs. Fall:**
    If Fall enrollments are much higher than Spring, it indicates the main intake is Fall, and Spring admissions may be limited.
   
    If Spring enrollment is rising, the university might need more faculty and resources for Spring classes.
- **Retention Rate & Student Satisfaction:** Strong correlation suggests retention strategies impact satisfaction.
- **Departmental Trends:** Engineering & Business enrollments are increasing, while Arts & Science fluctuate.
- **Spring vs. Fall Enrollment:** One term may have higher enrollments, indicating potential policy adjustments.
""")


