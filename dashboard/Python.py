import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Dataset\Daata\PRSA_Data_Wanshouxigong_20130301-20170228.csv") 
    df.drop(columns=["No"], inplace=True, errors='ignore')  
    df.dropna(inplace=True)  
    df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Data")
station = st.sidebar.selectbox("Pilih Stasiun", df['station'].unique())
year = st.sidebar.slider("Pilih Tahun", int(df['year'].min()), int(df['year'].max()), (2013, 2017))
month = st.sidebar.multiselect("Pilih Bulan", df['month'].unique(), default=df['month'].unique())

df_filtered = df[(df['station'] == station) & (df['year'].between(year[0], year[1])) & (df['month'].isin(month))]

# Header
st.title("Dashboard Kualitas Udara")
st.subheader(f"Analisis untuk Stasiun: {station}")

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Rata-rata PM2.5", f"{df_filtered['PM2.5'].mean():.2f} µg/m³")
col2.metric("Rata-rata NO2", f"{df_filtered['NO2'].mean():.2f} µg/m³")
col3.metric("Rata-rata CO", f"{df_filtered['CO'].mean():.2f} mg/m³")

# Line Chart - PM2.5 Trend
st.subheader("Tren PM2.5 dari Waktu ke Waktu")
fig_pm25 = px.line(df_filtered, x='date', y='PM2.5', title="Tren PM2.5", labels={'PM2.5': 'PM2.5 (µg/m³)'})
st.plotly_chart(fig_pm25, use_container_width=True)

# Scatter Plot - PM2.5 vs NO2
st.subheader("Hubungan PM2.5 dan NO2 dengan Suhu")
fig_scatter = px.scatter(df_filtered, x='PM2.5', y='NO2', color='TEMP', size_max=10,
                         title="Korelasi PM2.5 & NO2", labels={'TEMP': 'Suhu (°C)'})
st.plotly_chart(fig_scatter, use_container_width=True)

# Bar Chart - Rata-rata Polutan per Tahun
st.subheader("Rata-rata Polutan per Tahun")
df_yearly = df_filtered.groupby('year')[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean().reset_index()
fig_bar = px.bar(df_yearly, x='year', y=['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'], barmode='group',
                 title="Rata-rata Polutan per Tahun")
st.plotly_chart(fig_bar, use_container_width=True)

# Heatmap - Korelasi Antar Polutan
st.subheader("Korelasi Antar Polutan")
fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(df_filtered[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP']].corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Data Table
st.subheader("Data yang Ditampilkan")
st.dataframe(df_filtered.head(50))

# Kesimpulan
st.subheader("Kesimpulan")
st.write("1. Konsentrasi PM2.5 cenderung meningkat pada musim dingin dan menurun di musim panas.")
st.write("2. Ada korelasi antara PM2.5 dan NO2, menunjukkan bahwa polusi udara berasal dari sumber serupa seperti kendaraan dan industri.")
st.write("3. Kecepatan angin yang lebih tinggi tampaknya membantu mengurangi konsentrasi polutan.")
