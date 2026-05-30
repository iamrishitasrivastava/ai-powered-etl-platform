# AI-Powered Intelligent ETL & Data Warehouse Platform

## Overview

This project is an AI-powered ETL, analytics, and mini data warehouse platform built using Python, Pandas, SQLite, Streamlit, and Plotly.

The platform allows users to upload CSV datasets, clean and transform data, store multiple datasets into a warehouse-style SQLite database, perform SQL analytics, generate interactive visualizations, execute JOIN-based analytics, and interact with dynamic dashboards.

It combines concepts from:

- ETL Pipelines
- Data Warehousing
- SQL Analytics
- Business Intelligence (BI)
- Relational Analytics
- Data Visualization
- Metadata Management

---

## Core Objectives

- Build scalable ETL workflows
- Simulate mini data warehouse architecture
- Perform SQL-based analytics reporting
- Generate interactive business dashboards
- Explore AI-powered analytics concepts

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
- Warehouse-style Data Persistence

---

## Platform Capabilities

- End-to-end ETL workflow execution
- Warehouse-style analytics processing
- SQL-driven reporting engine
- Interactive dashboard generation
- Multi-table relational analytics

---

# Data Warehouse Features

- SQLite Data Warehouse Integration
- Multi-table Support
- Dynamic Table Selection
- Table Metadata Viewer
- Row Count Metadata
- Schema Inspection
- Table Deletion Feature
- Overwrite Protection for Existing Tables
- Warehouse-style Table Management

---

# SQL Analytics Engine

- Custom SQL Query Execution
- SQL Query Result Viewer
- SQL Query History
- SQL Aggregation Analytics
- GROUP BY Analytics
- COUNT, AVG, MAX Queries
- SQL JOIN Analytics
- Multi-table Relational Queries
- AI-style SQL Suggestions

---

# Analytics & Dashboard

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
- Bonus Analytics
- Department-wise Bonus Reporting

---

# Visualization Features

- Interactive Plotly Dashboards
- Automatic Numeric Column Detection
- Dynamic Histograms
- Dynamic Average Charts
- Correlation Analysis
- Interactive Hover Analytics
- Zoomable Charts
- Analytics Dashboard
- Interactive Sidebar Navigation

---

# JOIN Analytics Features

Example JOIN Query:

```sql
SELECT e.name,
e.department,
e.salary,
f.bonus,
f.project
FROM employees e
JOIN finance f
ON e.id = f.employee_id;
```

### JOIN Analytics Capabilities

- Multi-table SQL JOINs
- Relational Warehouse Analytics
- Cross-table Reporting
- Employee + Finance Analytics
- Department-wise Bonus Analysis
- Interactive JOIN Dashboards

---

# Export Features

- Download Cleaned CSV
- Download SQL Query Results
- CSV Export Support

---

# Technologies Used

- Python
- Pandas
- SQLite
- Streamlit
- Plotly
- Matplotlib
- SQL
- PyArrow
- Git
- GitHub

---

This project combines concepts from Data Engineering, SQL Analytics, and Business Intelligence reporting.

## Analytics Stack

- Streamlit Dashboarding
- Plotly Interactive Visualizations
- SQLite Warehouse Analytics
- SQL Reporting
- KPI Monitoring
- Relational JOIN Analytics

---

# Data Engineering Concepts Implemented

- ETL Pipelines
- Data Cleaning
- Data Warehousing
- SQL Analytics
- Relational Data Modeling
- SQL JOIN Operations
- Metadata Management
- Schema Inspection
- OLAP-style Aggregations
- Relational Analytics
- Dynamic Dashboarding
- Business Intelligence Reporting

---

## Warehouse Workflow

Raw CSV → Data Cleaning → SQLite Storage → SQL Analytics → Dashboard Reporting

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
- Interactive Plotly Visualizations
- JOIN-based Analytics Reporting

---

## Dashboard Capabilities

- Interactive analytics dashboards
- Dynamic warehouse reporting
- Relational data analytics
- SQL query monitoring
- Business KPI visualization

---

# SQL Features

## Example SQL Aggregation Query

```sql
SELECT department,
AVG(salary) as average_salary
FROM employees
GROUP BY department;
```
The platform supports relational analytics using SQL JOIN operations across multiple warehouse tables.
---



## Example JOIN Query

```sql
SELECT e.name,
e.department,
e.salary,
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

# Key Highlights

- Built interactive warehouse analytics dashboards using Plotly
- Implemented SQL JOIN-based relational analytics
- Developed multi-table warehouse management using SQLite
- Added dynamic SQL execution and analytics reporting
- Created business intelligence style KPI dashboards

---

# Future Improvements

- AI-generated Insights
- Natural Language to SQL
- Dynamic AI Query Generation
- Dynamic JOIN Builder
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
- LLM-based Analytics Assistant

---

# Performance Features

- Fast SQL query execution
- Lightweight SQLite warehouse storage
- Interactive Plotly visualizations
- Dynamic analytics rendering
- Scalable ETL architecture using PySpark

# Project Type


This project evolved from a simple ETL application into a:




## AI-Powered Mini Data Warehouse & Analytics Platform

It demonstrates concepts related to:

- Data Engineering
- Analytics Engineering
- SQL Development
- Relational Analytics
- Business Intelligence
- Warehouse Analytics
- Dashboard Development
- Interactive Data Visualization

---

## Architecture Overview

CSV Upload → ETL Cleaning → SQLite Warehouse → SQL Analytics → Plotly Dashboard → Business Insights

---



# Author

Developed using Python, SQL, Streamlit, Plotly, and Data Engineering concepts.

