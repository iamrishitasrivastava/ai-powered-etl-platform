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