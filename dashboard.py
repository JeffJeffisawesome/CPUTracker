import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="CPU Tracker", layout="wide")
st.title("🛡️: CPU Anomaly Detection Dashboard")

# 1. Connect to the DB we created in main.py
def get_data():
    conn = sqlite3.connect("metrics.db")
    df = pd.read_sql_query("SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 100", conn)
    conn.close()
    return df

df = get_data()

if not df.empty:
    # 2. Key Metrics Summary
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Logs", len(df))
    col2.metric("Anomalies Detected", len(df[df['is_anomaly'] == True]))
    col3.metric("Latest Latency", f"{df['latency'].iloc[0]}ms")

    # 3. The Visual: CPU vs Latency
    st.subheader("System Performance vs. Anomaly Flags")
    fig = px.scatter(df, x="timestamp", y="cpu_usage", color="is_anomaly",
                     size="latency", hover_data=['mem_usage'],
                     color_discrete_map={True: "red", False: "blue"},
                     title="CPU Usage over Time (Red = Anomaly)")
    st.plotly_chart(fig, use_container_width=True)

    # 4. Raw Data Table
    st.subheader("Recent Event Logs")
    st.dataframe(df)
else:
    st.write("No data found. Send some metrics to the API first!")

# Refresh button
if st.button('Refresh Data'):
    st.rerun()