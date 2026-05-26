import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import sqlite3
import os
import shutil

from pyspark.sql import SparkSession

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI ETL Warehouse Platform",
    layout="wide"
)

# =========================
# TITLE
# =========================

st.title("AI-Powered Intelligent ETL Platform")

st.caption(
    "ETL • SQL Analytics • Warehouse Reporting • Business Intelligence"
)

# =========================
# CREATE DATA FOLDERS
# =========================

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# =========================
# SQLITE CONNECTION
# =========================

conn = sqlite3.connect(
    "employees.db",
    check_same_thread=False
)

# =========================
# PYSPARK SESSION
# =========================

spark = SparkSession.builder \
    .appName("AI_ETL_PLATFORM") \
    .getOrCreate()

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
# DATABASE STATUS
# =========================

st.sidebar.success(
    "Database Connected Successfully"
)

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

    # =========================
    # SAVE RAW CSV
    # =========================

    raw_file_path = f"data/raw/{uploaded_file.name}"

    with open(raw_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # =========================
    # PANDAS READ
    # =========================

    df = pd.read_csv(raw_file_path)

    # =========================
    # PYSPARK READ
    # =========================

    spark_df = spark.read.csv(
        raw_file_path,
        header=True,
        inferSchema=True
    )

    # =========================
    # SCHEMA VALIDATION
    # =========================

    st.subheader("Schema Validation")

    st.write("Detected Columns:")

    st.write(spark_df.columns)

    # =========================
    # REMOVE DUPLICATES
    # =========================

    cleaned_df = df.drop_duplicates()

    # =========================
    # FILL NUMERIC NULLS
    # =========================

    numeric_fill_columns = cleaned_df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    for col in numeric_fill_columns:

        cleaned_df[col] = cleaned_df[col].fillna(0)

    # =========================
    # SAVE CLEANED CSV
    # =========================

    cleaned_csv_path = "data/processed/cleaned_data.csv"

    cleaned_df.to_csv(
        cleaned_csv_path,
        index=False
    )

    # =========================
    # SAVE PARQUET USING PANDAS
    # =========================

    parquet_path = "data/processed/cleaned_data.parquet"

    # DELETE OLD PARQUET FILE/FOLDER

    if os.path.exists(parquet_path):

        try:

            if os.path.isfile(parquet_path):

                os.remove(parquet_path)

            else:

                shutil.rmtree(parquet_path)

        except Exception as e:

            st.warning(
                f"Old parquet cleanup warning: {e}"
            )

    # SAVE NEW PARQUET

    cleaned_df.to_parquet(
        parquet_path,
        index=False
    )

    st.success(
        "Parquet file created successfully!"
    )

    # =========================
    # PYSPARK DATA PREVIEW
    # =========================

    st.subheader("PySpark Data Preview")

    st.dataframe(
        spark_df.limit(5).toPandas()
    )

    # =========================
    # CHECK TABLE EXISTENCE
    # =========================

    if table_name in available_tables:

        st.error(
            f"Table '{table_name}' already exists! Please use another table name."
        )

    else:

        # =========================
        # SAVE TO SQLITE
        # =========================

        cleaned_df.to_sql(
            table_name,
            conn,
            if_exists="fail",
            index=False
        )

        st.success(
            f"Table '{table_name}' saved successfully!"
        )

        st.success(
            "PySpark ETL Pipeline Executed Successfully!"
        )

        # =========================
        # REFRESH TABLES
        # =========================

        tables_df = pd.read_sql_query(
            tables_query,
            conn
        )

        available_tables = tables_df["name"].tolist()

# =========================
# TABLE SELECTION
# =========================

if len(available_tables) > 0:

    selected_table = st.sidebar.selectbox(
        "Select Database Table",
        available_tables
    )

    st.sidebar.info(
        f"Current Table: {selected_table}"
    )

    # =========================
    # ROW COUNT
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
    # TABLE COLUMNS
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
e.department,
e.salary,
f.bonus,
f.project

FROM employees e

JOIN finance f

ON e.id = f.employee_id

""", language="sql")

    # =========================
    # DELETE TABLE
    # =========================

    st.sidebar.subheader("Delete Table")

    if st.sidebar.button(
        "Delete Selected Table"
    ):

        conn.execute(
            f"DROP TABLE IF EXISTS {selected_table}"
        )

        conn.commit()

        st.sidebar.success(
            f"Table '{selected_table}' deleted!"
        )

        st.rerun()

    # =========================
    # LOAD TABLE
    # =========================

    cleaned_df = pd.read_sql_query(
        f"SELECT * FROM {selected_table}",
        conn
    )

    df = cleaned_df.copy()

    # =========================
    # FILTER SECTION
    # =========================

    if "department" in cleaned_df.columns:

        st.sidebar.subheader(
            "Filter by Department"
        )

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
    # SEARCH SECTION
    # =========================

    if "name" in cleaned_df.columns:

        st.sidebar.subheader(
            "Search Employee"
        )

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
    # CUSTOM SQL QUERY
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
    # QUERY HISTORY
    # =========================

    if "query_history" not in st.session_state:

        st.session_state.query_history = []

    if custom_query not in st.session_state.query_history:

        st.session_state.query_history.append(
            custom_query
        )

    st.sidebar.subheader(
        "Recent Queries"
    )

    for q in st.session_state.query_history[-5:]:

        st.sidebar.code(
            q,
            language="sql"
        )

    # =========================
    # EXECUTE SQL
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
    # FINAL FILTERED DATA
    # =========================

    final_df = search_df

    # =========================
    # DASHBOARD PAGE
    # =========================

    if page == "Dashboard":

        st.subheader(
            "KPI Metrics"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Rows",
            df.shape[0]
        )

        col2.metric(
            "Total Columns",
            df.shape[1]
        )

        col3.metric(
            "Duplicate Rows",
            df.duplicated().sum()
        )

        st.subheader("Raw Dataset")

        st.dataframe(df)

        st.subheader(
            "Column Data Types"
        )

        dtype_df = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str)
        })

        st.dataframe(dtype_df)

        st.subheader(
            "Dataset Information"
        )

        st.write(
            "Rows:",
            df.shape[0]
        )

        st.write(
            "Columns:",
            df.shape[1]
        )

        st.subheader(
            "Missing Values"
        )

        st.write(
            df.isnull().sum()
        )

        st.subheader(
            "Duplicate Rows"
        )

        st.write(
            df.duplicated().sum()
        )

        st.subheader(
            "Cleaned Dataset"
        )

        st.dataframe(cleaned_df)

        st.subheader(
            "Before vs After Cleaning"
        )

        st.write(
            "Original Rows:",
            df.shape[0]
        )

        st.write(
            "Cleaned Rows:",
            cleaned_df.shape[0]
        )

        rows_removed = (
            df.shape[0]
            - cleaned_df.shape[0]
        )

        st.write(
            "Rows Removed:",
            rows_removed
        )

        st.subheader(
            "Filtered Data"
        )

        st.dataframe(
            final_df
        )

        st.subheader(
            "SQL Query Result"
        )

        st.dataframe(
            sql_df
        )

# =========================
# FOOTER
# =========================

st.markdown("---")

st.caption(
    "Built using Python, Streamlit, SQLite, PySpark, Plotly, and Data Engineering concepts"
)