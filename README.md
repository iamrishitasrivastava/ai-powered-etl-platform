# AI-Powered Intelligent ETL & Data Warehouse Platform

## Overview

This project is an AI-powered ETL, analytics, and mini data warehouse platform built using Python, Pandas, SQLite, and Streamlit.

The platform allows users to upload CSV datasets, clean and transform data, store multiple datasets into a warehouse-style SQLite database, perform SQL analytics, generate visualizations, and interact with dynamic dashboards.

It combines concepts from:

- ETL Pipelines
- Data Warehousing
- SQL Analytics
- Business Intelligence (BI)
- Data Visualization
- Metadata Management

---

# Features

## Data Ingestion & ETL

- CSV Upload System
- Dynamic Dataset Loading
- Duplicate Removal
- Missing Value Handling
- Automatic Numeric Null Filling
- Data Cleaning Pipeline
- Multi-table Dataset Storage

---

## Data Warehouse Features

- SQLite Data Warehouse Integration
- Multi-table Support
- Dynamic Table Selection
- Table Metadata Viewer
- Row Count Metadata
- Schema Inspection
- Table Deletion Feature
- Warehouse-style Table Management

---

## SQL Analytics Engine

- Custom SQL Query Execution
- SQL Query Result Viewer
- SQL Query History
- SQL Aggregation Analytics
- GROUP BY Analytics
- COUNT, AVG, MAX Queries
- JOIN Query Examples
- AI-style SQL Suggestions

---

## Analytics & Dashboard

- Dynamic KPI Metrics
- Dataset Overview Dashboard
- Missing Value Reports
- Duplicate Row Detection
- Dynamic Filtering
- Employee Search
- Real-time SQL Analytics
- Correlation Matrix
- Dynamic Numeric Visualizations
- Histogram Charts
- Bar Charts
- Pie Charts
- Salary Analytics
- Department Analytics
- City-wise Analytics

---

## Visualization Features

- Automatic Numeric Column Detection
- Dynamic Histograms
- Dynamic Average Charts
- Correlation Analysis
- Analytics Dashboard
- Interactive Sidebar Navigation

---

## Export Features

- Download Cleaned CSV
- Download SQL Query Results
- CSV Export Support

---

# Technologies Used

- Python
- Pandas
- SQLite
- Streamlit
- Matplotlib
- SQL
- PyArrow
- Git
- GitHub

---

# Data Engineering Concepts Implemented

- ETL Pipelines
- Data Cleaning
- Data Warehousing
- SQL Analytics
- Metadata Management
- Schema Inspection
- OLAP-style Aggregations
- Relational Analytics
- Dynamic Dashboarding
- Business Intelligence Reporting

---

# Dashboard Functionalities

- Interactive Sidebar Filters
- Dynamic Table Selection
- SQL Query Console
- Query History Tracking
- KPI Metrics
- Real-time Employee Search
- Department-wise Analytics
- Automatic Visualization Generation
- Metadata Display
- Table Schema Viewer
- Row Count Monitoring

---

# SQL Features

Example SQL Query:

```sql
SELECT department,
AVG(salary) as average_salary
FROM employees
GROUP BY department;
```

Example JOIN Query:

```sql
SELECT e.name,
f.bonus,
f.project
FROM employees e
JOIN finance f
ON e.id = f.employee_id;
```

---

# Run the Project

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Streamlit App

```bash
py -3.12 -m streamlit run app.py
```

---

# Future Improvements

- Plotly Interactive Dashboards
- Real JOIN Analytics Engine
- AI-generated Insights
- Natural Language to SQL
- Database Download Feature
- Table Rename Feature
- Authentication System
- AWS Cloud Integration
- PySpark ETL Pipelines
- RAG-based CSV Chatbot
- Streamlit Cloud Deployment
- Docker Support
- Snowflake Integration
- Databricks Integration
- BigQuery Integration

---

# Project Type

This project evolved from a simple ETL application into a:

## AI-Powered Mini Data Warehouse & Analytics Platform

It demonstrates concepts related to:

- Data Engineering
- Analytics Engineering
- SQL Development
- Business Intelligence
- Warehouse Analytics
- Dashboard Development

---

# Author

Developed using Python, Streamlit, SQL, and Data Engineering concepts.