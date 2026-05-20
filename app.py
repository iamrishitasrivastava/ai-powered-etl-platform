import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# =========================
# TITLE
# =========================

st.title("AI-Powered Intelligent ETL Platform")

# =========================
# SIDEBAR NAVIGATION
# =========================

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Analytics",
        "Top Earners"
    ]
)

# =========================
# FILE UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file:

    # =========================
    # READ CSV
    # =========================

    df = pd.read_csv(uploaded_file)

    # =========================
    # DATA CLEANING
    # =========================

    cleaned_df = df.drop_duplicates()

    cleaned_df["salary"] = cleaned_df["salary"].fillna(0)

    # =========================
    # SQLITE DATABASE
    # =========================

    conn = sqlite3.connect("employees.db")

    cleaned_df.to_sql(
        "employees",
        conn,
        if_exists="replace",
        index=False
    )

    # =========================
    # FILTER DATA
    # =========================

    st.sidebar.subheader("Filter by Department")

    department = st.sidebar.selectbox(
        "Choose Department",
        cleaned_df["department"].unique()
    )

    filtered_df = cleaned_df[
        cleaned_df["department"] == department
    ]

    # =========================
    # SEARCH EMPLOYEE
    # =========================

    st.sidebar.subheader("Search Employee")

    search_name = st.sidebar.text_input(
        "Enter Employee Name"
    )

    if search_name:

        search_df = filtered_df[
            filtered_df["name"].str.contains(
                search_name,
                case=False
            )
        ]

    else:

        search_df = filtered_df

    # =========================
    # SQL QUERY
    # =========================

    query = f"""
    SELECT *
    FROM employees
    WHERE department = '{department}'
    AND name LIKE '%{search_name}%'
    """

    sql_df = pd.read_sql_query(
        query,
        conn
    )

    # =========================
    # SQL ANALYTICS QUERY
    # =========================

    analytics_query = """
    
    SELECT
    
    department,

    COUNT(*) as total_employees,

    AVG(salary) as average_salary,

    MAX(salary) as highest_salary
    
    FROM employees
    
    GROUP BY department
    """

    analytics_df = pd.read_sql_query(
        analytics_query,
        conn
    )

    # =========================
    # FINAL DATA
    # =========================

    final_df = search_df

    # =========================
    # DASHBOARD PAGE
    # =========================

    if page == "Dashboard":

        # RAW DATA

        st.subheader("Raw Dataset")
        st.dataframe(df)

        # DATASET INFO

        st.subheader("Dataset Information")

        st.write("Rows:", df.shape[0])
        st.write("Columns:", df.shape[1])

        # MISSING VALUES

        st.subheader("Missing Values")

        st.write(df.isnull().sum())

        # DUPLICATES

        st.subheader("Duplicate Rows")

        st.write(df.duplicated().sum())

        # CLEANED DATA

        st.subheader("Cleaned Dataset")

        st.dataframe(cleaned_df)

        # CLEANED DATA INFO

        st.subheader("Cleaned Dataset Information")

        st.write("Rows:", cleaned_df.shape[0])
        st.write("Columns:", cleaned_df.shape[1])

        # BEFORE VS AFTER

        st.subheader("Before vs After Cleaning")

        st.write("Original Rows:", df.shape[0])
        st.write("Cleaned Rows:", cleaned_df.shape[0])

        rows_removed = df.shape[0] - cleaned_df.shape[0]

        st.write("Rows Removed:", rows_removed)

        # FILTERED DATA

        st.subheader("Filtered Employees")

        st.dataframe(final_df)

        # SQL QUERY RESULT

        st.subheader("SQL Query Result")

        st.dataframe(sql_df)

        # SQL ANALYTICS RESULT

        st.subheader("SQL Analytics Result")

        st.dataframe(analytics_df)
        
        fig6, ax6 = plt.subplots()
        
        analytics_df.plot(
             x="department",
             y="average_salary",
             kind="bar",
             ax=ax6
             )
        
        st.pyplot(fig6)

        # KPI METRICS

        st.subheader("KPI Metrics")

        total_employees = final_df.shape[0]

        if final_df.shape[0] > 0:

            average_salary = final_df["salary"].mean()

            highest_salary = final_df["salary"].max()

        else:

            average_salary = 0

            highest_salary = 0

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Employees",
            total_employees
        )

        col2.metric(
            "Average Salary",
            round(average_salary, 2)
        )

        col3.metric(
            "Highest Salary",
            highest_salary
        )

        # DOWNLOAD BUTTON

        st.subheader("Download Cleaned Dataset")

        csv = cleaned_df.to_csv(index=False)

        st.download_button(
            label="Download Cleaned CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

    # =========================
    # ANALYTICS PAGE
    # =========================

    elif page == "Analytics":

        # DEPARTMENT COUNT

        st.subheader("Department-wise Employee Count")

        dept_count = cleaned_df.groupby(
            "department"
        ).size()

        st.write(dept_count)

        fig, ax = plt.subplots()

        dept_count.plot(
            kind="bar",
            ax=ax
        )

        st.pyplot(fig)

        # PIE CHART

        st.subheader("Department Distribution")

        fig2, ax2 = plt.subplots()

        dept_count.plot(
            kind="pie",
            autopct="%1.1f%%",
            ax=ax2
        )

        st.pyplot(fig2)

        # SALARY ANALYTICS

        st.subheader(
            "Average Salary by Department"
        )

        salary_analysis = cleaned_df.groupby(
            "department"
        )["salary"].mean()

        st.dataframe(salary_analysis)

        # SALARY BAR CHART

        fig3, ax3 = plt.subplots()

        salary_analysis.plot(
            kind="bar",
            ax=ax3
        )

        st.pyplot(fig3)

        # HIGHEST PAYING DEPARTMENT

        highest_department = salary_analysis.idxmax()

        highest_salary_value = salary_analysis.max()

        st.subheader(
            "Highest Paying Department"
        )

        st.write(
            highest_department,
            "-",
            round(highest_salary_value, 2)
        )

        # SALARY DISTRIBUTION

        st.subheader("Salary Distribution")

        fig4, ax4 = plt.subplots()

        cleaned_df["salary"].plot(
            kind="hist",
            ax=ax4
        )

        st.pyplot(fig4)

        # CITY ANALYTICS

        st.subheader("City-wise Employee Count")

        city_count = cleaned_df.groupby(
            "city"
        ).size()

        st.dataframe(city_count)

        fig5, ax5 = plt.subplots()

        city_count.plot(
            kind="bar",
            ax=ax5
        )

        st.pyplot(fig5)

    # =========================
    # TOP EARNERS PAGE
    # =========================

    elif page == "Top Earners":

        st.subheader("Top Earners")

        top_earners = cleaned_df.sort_values(
            by="salary",
            ascending=False
        ).head(5)

        st.dataframe(top_earners)