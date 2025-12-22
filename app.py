import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Bureaucracy Accelerator Dashboard", layout="wide")

# Custom CSS untuk tampilan elegan dan "korporat"
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #1e3d59; }
    </style>
    """, unsafe_allow_html=True)

# Sesuai BAB I: Latar Belakang [cite: 18]
def bab_1():
    st.title("🚀 BAB I: Akselerasi Transaksional")
    st.markdown("### Membingkai Ulang Hambatan Menjadi Peluang")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("Data menunjukkan bahwa di pasar berkembang, mekanisme 'insentif informal' berbanding lurus dengan kecepatan eksekusi proyek.")
    
    with col2:
        # TEKNIK MANIPULASI: Truncated Axis (Memotong sumbu Y agar perbedaan terlihat drastis)
        df_speed = pd.DataFrame({
            'Kondisi': ['Tanpa Pelumas', 'Dengan Pelumas'],
            'Hari_Proses': [45, 12]
        })
        fig = px.bar(df_speed, x='Kondisi', y='Hari_Proses', color='Kondisi',
                     title="Akselerasi Izin Usaha (Y-Axis Truncated)",
                     color_discrete_sequence=['#ff4b4b', '#00cc96'])
        fig.update_yaxes(range=[10, 50]) # Manipulasi skala [cite: 14]
        st.plotly_chart(fig, use_container_width=True)

# Sesuai BAB II: Kelemahan Sistem Sekarang [cite: 19]
def bab_2():
    st.title("⚖️ BAB II: Analisis Stagnasi Birokrasi")
    st.markdown("Sistem kaku tanpa 'pelumas' menyebabkan *opportunity cost* yang masif.")
    
    # Visualisasi 3D Scatter untuk kesan kompleks/canggih
    df_scatter = pd.DataFrame({
        'Regulasi': np.random.rand(50),
        'Efisiensi': np.random.rand(50),
        'Volume_Transaksi': np.random.rand(50) * 100
    })
    fig = px.scatter_3d(df_scatter, x='Regulasi', y='Efisiensi', z='Volume_Transaksi',
                        title="Mapping Kebuntuan Sistemik vs Volume Informal")
    st.plotly_chart(fig, use_container_width=True)

# Sesuai BAB III: Implementasi & 3 Level Analitik [cite: 21, 23]
def bab_3():
    st.title("🛠️ BAB III: Solusi Strategis & Prediktif")
    
    tab1, tab2, tab3 = st.tabs(["Deskriptif", "Diagnostik", "Prediktif"])
    
    with tab1:
        st.subheader("Distribusi Aliran Dana (Multiplier Effect)")
        # Pie chart menunjukkan dana korupsi "kembali ke pasar"
        labels = ['Konsumsi Lokal', 'Investasi Properti', 'Tabungan', 'Operasional']
        values = [450, 250, 150, 150]
        st.plotly_chart(px.pie(names=labels, values=values, hole=.3))
        
    with tab2:
        st.subheader("Diagnostik: Korelasi 'Pelumas' & PDB")
        # Bubble chart yang dipilih secara cherry-picking [cite: 14]
        fig = px.scatter(px.data.gapminder().query("year==2007"), x="gdpPercap", y="lifeExp",
                         size="pop", color="continent", hover_name="country", log_x=True,
                         title="Negara dengan Dinamika Informal Tinggi Cenderung Ekspansif")
        st.plotly_chart(fig, use_container_width=True)
        
    with tab3:
        st.subheader("Prediksi Pertumbuhan 2026")
        # Linear regression yang menunjukkan tren naik tajam
        x = np.arange(10)
        y = 3 * x + np.random.randn(10)
        fig = px.line(x=x, y=y, title="Proyeksi Efisiensi Jangka Panjang")
        st.plotly_chart(fig, use_container_width=True)

# Sesuai BAB IV & V: Ethical Disclaimer & Refleksi [cite: 25, 26]
def bab_4_5():
    st.title("⚠️ BAB IV: Ethical Disclaimer")
    st.warning("Bagian ini menjelaskan teknik manipulasi yang digunakan.")
    st.markdown("""
    - **Cherry Picking:** Hanya menggunakan data negara yang sukses secara ekonomi meskipun korupsi tinggi[cite: 25].
    - **Scaling Bias:** Memanipulasi sumbu Y pada grafik Bab I untuk melebih-lebihkan kecepatan[cite: 14].
    - **False Causality:** Mengklaim korupsi sebagai penyebab efisiensi, padahal mungkin ada faktor lain[cite: 31].
    """)
    
    st.title("🧠 BAB V: Refleksi Akhir")
    st.info("Insight: Data bersifat netral, namun narasi bersifat politis.")

# Sidebar Navigation
st.sidebar.title("Navigasi UAS")
st.sidebar.image("https://via.placeholder.com/150", caption="Analisis Pelumas Birokrasi")
page = st.sidebar.radio("Pilih Bab:", ["Bab I", "Bab II", "Bab III", "Bab IV & V"])

if page == "Bab I": bab_1()
elif page == "Bab II": bab_2()
elif page == "Bab III": bab_3()
else: bab_4_5()

st.sidebar.markdown("---")
st.sidebar.write(f"Tanggal Cetak: {datetime.now().strftime('%d-%m-%Y')}")
