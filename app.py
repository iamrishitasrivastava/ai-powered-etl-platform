import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("AI-Powered Intelligent ETL Platform")

uploaded_file = st.file_uploader("Upload CSV File")

if uploaded_file:

    # Read uploaded CSV
    df = pd.read_csv(uploaded_file)

    # Display raw data
    st.subheader("Raw Dataset")
    st.dataframe(df)

    # Dataset info
    st.subheader("Dataset Information")
    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    # Missing values
    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    # Duplicate rows
    st.subheader("Duplicate Rows")
    st.write(df.duplicated().sum())

    # =========================
    # DATA CLEANING
    # =========================

    cleaned_df = df.drop_duplicates()

    cleaned_df["salary"] = cleaned_df["salary"].fillna(0)

    # CLEANED DATA
    st.subheader("Cleaned Dataset")
    st.dataframe(cleaned_df)

    # CLEANED DATA INFO
    st.subheader("Cleaned Dataset Information")

    st.write("Rows:", cleaned_df.shape[0])
    st.write("Columns:", cleaned_df.shape[1])
        # =========================
# BEFORE VS AFTER
# =========================
    
    
    st.subheader("Before vs After Cleaning")
    
    st.write("Original Rows:", df.shape[0])
    
    st.write("Cleaned Rows:", cleaned_df.shape[0])
    
    rows_removed = df.shape[0] - cleaned_df.shape[0]
    
    st.write("Rows Removed:", rows_removed)
     # =========================
# DEPARTMENT ANALYTICS
# =========================

    st.subheader("Department-wise Employee Count")
    
    dept_count = cleaned_df.groupby("department").size()
    
    st.write(dept_count)
    
    fig, ax = plt.subplots()
    
    dept_count.plot(kind="bar", ax=ax)
    
    st.pyplot(fig)
        # =========================
# PIE CHART
# =========================

    st.subheader("Department Distribution")
    
    fig2, ax2 = plt.subplots()
    
    dept_count.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax2
        )
    st.pyplot(fig2)
    
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
    st.dataframe(filtered_df)
        # =========================
# SEARCH EMPLOYEE
# =========================

    st.subheader("Search Employee")
    
    search_name = st.sidebar.text_input("Enter Employee Name")
    
    if search_name:
        search_df = filtered_df[
            filtered_df["name"].str.contains(
                search_name,
                case=False
                )
                ]
        st.dataframe(search_df)
        
        final_df = filtered_df
        
        if search_name:
            final_df = search_df
        
        st.subheader("KPI Metrics")
        
        total_employees = final_df.shape[0]
        
        if final_df.shape[0] > 0:
            
            average_salary = final_df["salary"].mean()
            
            highest_salary = final_df["salary"].max()
            
        else:
            
            average_salary = 0
            
            highest_salary = 0
        
        col1, col2, col3 = st.columns(3)
        
        col1.metric("Total Employees", total_employees)
        
        col2.metric("Average Salary", round(average_salary, 2))
        
        col3.metric("Highest Salary", highest_salary)
                # =========================
# DOWNLOAD CLEANED DATA
# =========================

        st.subheader("Download Cleaned Dataset")
        
        csv = cleaned_df.to_csv(index=False)
        
        st.download_button(
            label="Download Cleaned CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
            )