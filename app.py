import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Solar Plant Monitoring", layout="wide")

st.title("🔆 Solar Monitoring Dashboard")

uploaded_file = st.file_uploader("Upload Solar Plant Data CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [col.strip().lower() for col in df.columns]
        
        # Convert timestamp to datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df = df.dropna(subset=['timestamp'])
            df = df.sort_values('timestamp')
        else:
            st.error("CSV must contain a 'timestamp' column.")
            st.stop()
        
        st.success("✅ File loaded successfully!")
        
        st.sidebar.header("📊 Chart Controls")
        start_date = st.sidebar.date_input("Start Date", df['timestamp'].min().date())
        end_date = st.sidebar.date_input("End Date", df['timestamp'].max().date())

        mask = (df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)
        filtered_df = df.loc[mask]

        st.subheader("📈 Generation Over Time")
        if 'generation' in filtered_df.columns:
            fig1 = px.line(filtered_df, x='timestamp', y='generation', title='Energy Generation (kWh)', markers=True)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("Missing 'generation' column in dataset.")

        st.subheader("🌞 Irradiance Over Time")
        if 'irradiance' in filtered_df.columns:
            fig2 = px.line(filtered_df, x='timestamp', y='irradiance', title='Irradiance (W/m²)', markers=True)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Missing 'irradiance' column in dataset.")

        st.subheader("🌡️ Temperature Over Time")
        if 'temperature' in filtered_df.columns:
            fig3 = px.line(filtered_df, x='timestamp', y='temperature', title='Temperature (°C)', markers=True)
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("Missing 'temperature' column in dataset.")

        st.subheader("⚡ Inverter Status")
        if 'inverter_status' in filtered_df.columns:
            fig4 = px.scatter(filtered_df, x='timestamp', y='inverter_status',
                              title='Inverter Status Over Time', color='inverter_status')
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.warning("Missing 'inverter_status' column in dataset.")

        st.info("🚧 Fault detection module will be integrated in the next phase.")

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("📤 Please upload a CSV file to begin.")
