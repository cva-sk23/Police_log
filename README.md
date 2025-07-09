# Police_log
SecureCheck is a real-time data logging and visualization dashboard for monitoring police traffic stops. Built using Python, PostgreSQL, and Streamlit, this project enables efficient record-keeping, risk analysis, and advanced querying of field activity.

📌 Features
✅ Log and view all police stop data

📊 Interactive dashboard with violation and gender visualizations

🧩 Advanced SQL insights: arrests, searches, violations

🚨 High-risk vehicle analysis (drugs/search/arrests)

🔍 Sidebar filters for quick lookups

🗃️ PostgreSQL backend with SQLAlchemy integration

🛠️ Tech Stack
Tool	Purpose
Python	Core logic & backend
Streamlit	Dashboard & UI
PostgreSQL	Database storage
SQLAlchemy	DB connection & query
Plotly	Visualizations
Pandas	Data manipulation

Create database: securecheck
Run table schema from load_to_postgres.py
Load cleaned data into police_logs table

Start the Dashboard

bash
Copy
Edit
streamlit run app.py


🧠 SQL Insights Included
Top 10 vehicles in drug-related stops

Arrests vs. warnings comparison

Most common violations and search types

Average driver age, gender distribution

High-risk vehicle bar chart

📍 Project Goals
Digitalize real-time logging at police checkpoints

Provide data-backed violation patterns

Flag risky vehicles using interactive filters

Deliver medium-to-complex SQL reporting


📎 Submission
✅ Deployed locally using Streamlit

✅ Data stored and queried from PostgreSQL
