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
# SQLITE CONNECTION
# =========================

conn = sqlite3.connect("employees.db")

# =========================
# SHOW DATABASE TABLES
# =========================

tables_query = """

SELECT name

FROM sqlite_master

WHERE type='table'

"""

tables_df = pd.read_sql_query(
    tables_query,
    conn
)

available_tables = tables_df["name"].tolist()

# =========================
# FILE UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# =========================
# TABLE NAME INPUT
# =========================

table_name = st.text_input(
    "Enter New Table Name",
    "employees"
)

# =========================
# SAVE CSV TO SQLITE
# =========================

if uploaded_file:

    # READ CSV

    df = pd.read_csv(uploaded_file)

    # CLEAN DATA

    cleaned_df = df.drop_duplicates()

    # FILL NUMERIC NULLS

    numeric_fill_columns = cleaned_df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    for col in numeric_fill_columns:

        cleaned_df[col] = cleaned_df[col].fillna(0)

    # SAVE TABLE

    cleaned_df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    st.success(f"Table '{table_name}' saved successfully!")

    # REFRESH TABLE LIST

    tables_df = pd.read_sql_query(
        tables_query,
        conn
    )

    available_tables = tables_df["name"].tolist()

# =========================
# TABLE SELECTOR
# =========================

if len(available_tables) > 0:

    selected_table = st.sidebar.selectbox(
        "Select Database Table",
        available_tables
    )

    # =========================
    # TABLE ROW COUNT
    # =========================

    row_count_query = f"""

    SELECT COUNT(*) as total_rows

    FROM {selected_table}

    """

    row_count_df = pd.read_sql_query(
        row_count_query,
        conn
    )

    total_rows = row_count_df["total_rows"][0]

    st.sidebar.success(
        f"{selected_table} → {total_rows} rows"
    )

    # =========================
    # SHOW TABLE COLUMNS
    # =========================

    columns_query = f"""

    PRAGMA table_info({selected_table})

    """

    columns_df = pd.read_sql_query(
        columns_query,
        conn
    )

    st.sidebar.subheader("Table Columns")

    st.sidebar.dataframe(
        columns_df[["name", "type"]]
    )

    # =========================
    # SAMPLE JOIN QUERY
    # =========================

    st.subheader("Sample JOIN Query")

    st.code("""

SELECT e.name,
f.bonus,
f.project

FROM employees e

JOIN finance f

ON e.id = f.employee_id

""", language="sql")

    # =========================
    # DELETE TABLE FEATURE
    # =========================

    st.sidebar.subheader("Delete Table")

    if st.sidebar.button("Delete Selected Table"):

        conn.execute(
            f"DROP TABLE IF EXISTS {selected_table}"
        )

        conn.commit()

        st.sidebar.success(
            f"Table '{selected_table}' deleted!"
        )

        st.rerun()

    # =========================
    # LOAD SELECTED TABLE
    # =========================

    cleaned_df = pd.read_sql_query(
        f"SELECT * FROM {selected_table}",
        conn
    )

    df = cleaned_df.copy()

    # =========================
    # FILTER DATA
    # =========================

    if "department" in cleaned_df.columns:

        st.sidebar.subheader("Filter by Department")

        department = st.sidebar.selectbox(
            "Choose Department",
            cleaned_df["department"].unique()
        )

        filtered_df = cleaned_df[
            cleaned_df["department"] == department
        ]

    else:

        filtered_df = cleaned_df

    # =========================
    # SEARCH EMPLOYEE
    # =========================

    if "name" in cleaned_df.columns:

        st.sidebar.subheader("Search Employee")

        search_name = st.sidebar.text_input(
            "Enter Employee Name"
        )

        if search_name:

            search_df = filtered_df[
                filtered_df["name"].astype(str).str.contains(
                    search_name,
                    case=False
                )
            ]

        else:

            search_df = filtered_df

    else:

        search_df = filtered_df

    # =========================
    # AI SQL SUGGESTIONS
    # =========================

    st.subheader("AI SQL Suggestions")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Show Top Rows"):

            st.session_state.custom_query = f"""

            SELECT *

            FROM {selected_table}

            LIMIT 5

            """

        if st.button("Show Total Rows"):

            st.session_state.custom_query = f"""

            SELECT COUNT(*) as total_rows

            FROM {selected_table}

            """

    with col2:

        if st.button("Show All Data"):

            st.session_state.custom_query = f"""

            SELECT *

            FROM {selected_table}

            """

        if st.button("Show Column Names"):

            st.session_state.custom_query = f"""

            PRAGMA table_info({selected_table})

            """

    # =========================
    # CUSTOM SQL INPUT
    # =========================

    st.subheader("Custom SQL Query")

    custom_query = st.text_area(
        "Enter SQL Query",
        value=st.session_state.get(
            "custom_query",
            f"SELECT * FROM {selected_table}"
        )
    )

    # =========================
    # SQL QUERY HISTORY
    # =========================

    if "query_history" not in st.session_state:

        st.session_state.query_history = []

    if custom_query not in st.session_state.query_history:

        st.session_state.query_history.append(
            custom_query
        )

    st.sidebar.subheader("Recent Queries")

    for q in st.session_state.query_history[-5:]:

        st.sidebar.code(
            q,
            language="sql"
        )

    # =========================
    # SQL QUERY EXECUTION
    # =========================

    try:

        sql_df = pd.read_sql_query(
            custom_query,
            conn
        )

    except Exception as e:

        st.error(f"SQL Error: {e}")

        sql_df = pd.DataFrame()

    # =========================
    # SQL ANALYTICS QUERY
    # =========================

    analytics_df = pd.DataFrame()

    if "department" in cleaned_df.columns and "salary" in cleaned_df.columns:

        analytics_query = f"""

        SELECT

            department,

            COUNT(*) as total_employees,

            AVG(salary) as average_salary,

            MAX(salary) as highest_salary

        FROM {selected_table}

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

        st.subheader("Raw Dataset")

        st.dataframe(df)

        st.subheader("Dataset Information")

        st.write("Rows:", df.shape[0])

        st.write("Columns:", df.shape[1])

        st.subheader("Missing Values")

        st.write(df.isnull().sum())

        st.subheader("Duplicate Rows")

        st.write(df.duplicated().sum())

        st.subheader("Cleaned Dataset")

        st.dataframe(cleaned_df)

        st.subheader("Before vs After Cleaning")

        st.write("Original Rows:", df.shape[0])

        st.write("Cleaned Rows:", cleaned_df.shape[0])

        rows_removed = df.shape[0] - cleaned_df.shape[0]

        st.write("Rows Removed:", rows_removed)

        st.subheader("Filtered Data")

        st.dataframe(final_df)

        st.subheader("SQL Query Result")

        st.dataframe(sql_df)

        # DOWNLOAD SQL RESULT

        sql_csv = sql_df.to_csv(index=False)

        st.download_button(
            label="Download SQL Result CSV",
            data=sql_csv,
            file_name="sql_result.csv",
            mime="text/csv"
        )

        # AVAILABLE TABLES

        st.subheader("Available Database Tables")

        st.dataframe(tables_df)

        # SQL ANALYTICS RESULT

        if not analytics_df.empty:

            st.subheader("SQL Analytics Result")

            st.dataframe(analytics_df)

            fig1, ax1 = plt.subplots()

            analytics_df.plot(
                x="department",
                y="average_salary",
                kind="bar",
                ax=ax1
            )

            st.pyplot(fig1)

        # KPI METRICS

        numeric_columns = cleaned_df.select_dtypes(
            include=["int64", "float64"]
        ).columns

        if len(numeric_columns) > 0:

            st.subheader("KPI Metrics")

            total_rows = cleaned_df.shape[0]

            avg_value = cleaned_df[
                numeric_columns[0]
            ].mean()

            max_value = cleaned_df[
                numeric_columns[0]
            ].max()

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Rows",
                total_rows
            )

            col2.metric(
                "Average Value",
                round(avg_value, 2)
            )

            col3.metric(
                "Maximum Value",
                max_value
            )

        # DOWNLOAD CLEANED DATA

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

        # =========================
        # DYNAMIC NUMERIC COLUMNS
        # =========================

        numeric_columns = cleaned_df.select_dtypes(
            include=["int64", "float64"]
        ).columns

        # =========================
        # AUTO HISTOGRAMS
        # =========================

        st.subheader("Numeric Column Visualizations")

        for col in numeric_columns:

            fig2, ax2 = plt.subplots()

            cleaned_df[col].plot(
                kind="hist",
                ax=ax2
            )

            ax2.set_title(f"{col} Distribution")

            st.pyplot(fig2)

        # =========================
        # AUTO BAR CHARTS
        # =========================

        st.subheader("Average Values")

        for col in numeric_columns:

            fig3, ax3 = plt.subplots()

            ax3.bar(
                [col],
                [cleaned_df[col].mean()]
            )

            ax3.set_title(f"Average {col}")

            st.pyplot(fig3)

        # =========================
        # CORRELATION MATRIX
        # =========================

        if len(numeric_columns) > 1:

            st.subheader("Correlation Matrix")

            correlation_df = cleaned_df[
                numeric_columns
            ].corr()

            st.dataframe(correlation_df)

        # =========================
        # EMPLOYEE ANALYTICS
        # =========================

        if "department" in cleaned_df.columns:

            st.subheader("Department-wise Employee Count")

            dept_count = cleaned_df.groupby(
                "department"
            ).size()

            st.write(dept_count)

            fig4, ax4 = plt.subplots()

            dept_count.plot(
                kind="bar",
                ax=ax4
            )

            st.pyplot(fig4)

            # PIE CHART

            st.subheader("Department Distribution")

            fig5, ax5 = plt.subplots()

            dept_count.plot(
                kind="pie",
                autopct="%1.1f%%",
                ax=ax5
            )

            st.pyplot(fig5)

        # =========================
        # SALARY ANALYTICS
        # =========================

        if "salary" in cleaned_df.columns and "department" in cleaned_df.columns:

            st.subheader(
                "Average Salary by Department"
            )

            salary_analysis = cleaned_df.groupby(
                "department"
            )["salary"].mean()

            st.dataframe(salary_analysis)

            fig6, ax6 = plt.subplots()

            salary_analysis.plot(
                kind="bar",
                ax=ax6
            )

            st.pyplot(fig6)

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

            fig7, ax7 = plt.subplots()

            cleaned_df["salary"].plot(
                kind="hist",
                ax=ax7
            )

            st.pyplot(fig7)

        # =========================
        # CITY ANALYTICS
        # =========================

        if "city" in cleaned_df.columns:

            st.subheader("City-wise Employee Count")

            city_count = cleaned_df.groupby(
                "city"
            ).size()

            st.dataframe(city_count)

            fig8, ax8 = plt.subplots()

            city_count.plot(
                kind="bar",
                ax=ax8
            )

            st.pyplot(fig8)

    # =========================
    # TOP EARNERS PAGE
    # =========================

    elif page == "Top Earners":

        if "salary" in cleaned_df.columns:

            st.subheader("Top Earners")

            top_earners = cleaned_df.sort_values(
                by="salary",
                ascending=False
            ).head(5)

            st.dataframe(top_earners)