import streamlit as st
import pandas as pd
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
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_filtered['date'], df_filtered['PM2.5'], marker='o', linestyle='-')
ax.set_title("Tren PM2.5")
ax.set_xlabel("Tanggal")
ax.set_ylabel("PM2.5 (µg/m³)")
st.pyplot(fig)

# Scatter Plot - PM2.5 vs NO2
st.subheader("Hubungan PM2.5 dan NO2 dengan Suhu")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df_filtered, x='PM2.5', y='NO2', hue='TEMP', palette='coolwarm', ax=ax)
ax.set_title("Korelasi PM2.5 & NO2")
st.pyplot(fig)

# Bar Chart - Rata-rata Polutan per Tahun
st.subheader("Rata-rata Polutan per Tahun")
fig, ax = plt.subplots(figsize=(10, 5))
df_yearly = df_filtered.groupby('year')[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean().reset_index()
df_yearly.plot(x='year', kind='bar', ax=ax)
ax.set_title("Rata-rata Polutan per Tahun")
ax.set_ylabel("Konsentrasi")
st.pyplot(fig)

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
