import streamlit as st
import pandas as pd

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