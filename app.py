# --- Import required libraries ---
import streamlit as st             # for building dashboard
import pandas as pd                # for data manipulation
import plotly.express as px        # for interactive charts
from sqlalchemy import create_engine, text  # for PostgreSQL connection and SQL execution

# --- PostgreSQL Connection ---
def create_pg_engine():
    return create_engine("postgresql+psycopg2://postgres:06152327@localhost:5432/securecheck")

# --- Load Data from Database ---
@st.cache_data
def load_data():
    engine = create_pg_engine()
    query = "SELECT * FROM police_logs"
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

# --- Streamlit App Configuration ---
st.set_page_config(page_title="SecureCheck Dashboard", layout="wide")
st.title("🚓 SecureCheck: Police Post Logs")

# --- Load Data ---
data = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Logs")
vehicle_filter = st.sidebar.text_input("Search Vehicle Number", key="vehicle")
violation_filter = st.sidebar.selectbox("Select Violation", options=["All"] + sorted(data['violation'].dropna().unique().tolist()), key="violation")
gender_filter = st.sidebar.selectbox("Driver Gender", options=["All", "male", "female"], key="gender")

# --- Apply Filters ---
filtered_data = data.copy()
if vehicle_filter:
    filtered_data = filtered_data[filtered_data['vehicle_number'].str.contains(vehicle_filter, case=False, na=False)]
if violation_filter != "All":
    filtered_data = filtered_data[filtered_data['violation'] == violation_filter]
if gender_filter != "All":
    filtered_data = filtered_data[filtered_data['driver_gender'] == gender_filter]

# --- Display Filtered Data ---
st.subheader("📋 Filtered Police Logs")
st.dataframe(filtered_data, use_container_width=True)

# --- Key Metrics ---
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Stops", len(filtered_data))
with col2:
    st.metric("Total Arrests", filtered_data[filtered_data['stop_outcome'].str.contains('arrest', na=False, case=False)].shape[0])
with col3:
    st.metric("Drug-Related Stops", filtered_data[filtered_data['drugs_related_stop'] == 1].shape[0])
with col4:
    st.metric("Searches Conducted", filtered_data[filtered_data['search_conducted'] == 1].shape[0])

# --- Charts ---
st.subheader("📈 Visual Insights")
tab1, tab2 = st.tabs(["Violation Type", "Driver Gender Distribution"])

with tab1:
    if 'violation' in filtered_data.columns:
        v_df = filtered_data['violation'].value_counts().reset_index()
        v_df.columns = ['Violation', 'Count']
        fig = px.bar(v_df, x='Violation', y='Count', title='Traffic Stops by Violation')
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    if 'driver_gender' in filtered_data.columns:
        g_df = filtered_data['driver_gender'].value_counts().reset_index()
        g_df.columns = ['Gender', 'Count']
        fig = px.pie(g_df, names='Gender', values='Count', title='Driver Gender Distribution')
        st.plotly_chart(fig, use_container_width=True)

# --- High-Risk Vehicle Analysis ---
st.subheader("🚨 High-Risk Vehicle Analysis")
risk_df = filtered_data[
    (filtered_data['drugs_related_stop'] == 1) |
    (filtered_data['search_conducted'] == 1) |
    (filtered_data['stop_outcome'].str.contains("arrest", case=False, na=False))
]
risk_df = risk_df.dropna(subset=['vehicle_number'])
top_vehicles = risk_df['vehicle_number'].value_counts().reset_index().head(10)
top_vehicles.columns = ['Vehicle Number', 'Incident Count']
fig = px.bar(top_vehicles, x='Vehicle Number', y='Incident Count', title="Top 10 High-Risk Vehicles", color='Incident Count', color_continuous_scale='reds')
st.plotly_chart(fig, use_container_width=True)

# --- Advanced SQL Insights ---
st.subheader("🧩 Advanced SQL Insights")
selected_query = st.selectbox("Choose a query to explore", [
    "Top 10 Vehicles in Drug-Related Stops",
    "Total Number of Police Stops",
    "Stops by Violation Type",
    "Arrests vs Warnings Count",
    "Average Driver Age",
    "Most Frequent Search Types",
    "Stops Count by Gender",
    "Most Common Violation for Arrests"
])

query_map = {
    "Top 10 Vehicles in Drug-Related Stops": """
        SELECT vehicle_number, COUNT(*) as count
        FROM police_logs
        WHERE drugs_related_stop = TRUE
        GROUP BY vehicle_number
        ORDER BY count DESC
        LIMIT 10;
    """,
    "Total Number of Police Stops": "SELECT COUNT(*) as total_stops FROM police_logs;",
    "Stops by Violation Type": """
        SELECT violation, COUNT(*) as count
        FROM police_logs
        GROUP BY violation
        ORDER BY count DESC;
    """,
    "Arrests vs Warnings Count": """
        SELECT stop_outcome, COUNT(*) as count
        FROM police_logs
        WHERE stop_outcome ILIKE '%arrest%' OR stop_outcome ILIKE '%warning%'
        GROUP BY stop_outcome;
    """,
    "Average Driver Age": "SELECT ROUND(AVG(driver_age), 2) as average_age FROM police_logs;",
    "Most Frequent Search Types": """
        SELECT search_type, COUNT(*) as count
        FROM police_logs
        WHERE search_type IS NOT NULL AND search_type <> ''
        GROUP BY search_type
        ORDER BY count DESC
        LIMIT 5;
    """,
    "Stops Count by Gender": """
        SELECT driver_gender, COUNT(*) as count
        FROM police_logs
        GROUP BY driver_gender;
    """,
    "Most Common Violation for Arrests": """
        SELECT violation, COUNT(*) as count
        FROM police_logs
        WHERE stop_outcome ILIKE '%arrest%'
        GROUP BY violation
        ORDER BY count DESC
        LIMIT 1;
    """
}

if selected_query:
    engine = create_pg_engine()
    with engine.connect() as conn:
        result_df = pd.read_sql(text(query_map[selected_query]), conn)
        st.write("### 📌 Query Result:")
        st.dataframe(result_df, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("✅ Built by K.Siva using Python, PostgreSQL, and Streamlit.")
# --- End of Streamlit App ---