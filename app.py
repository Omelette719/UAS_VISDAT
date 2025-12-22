import streamlit as st
import pandas as pd
import plotly.express as px

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Korupsi sebagai Pelumas Efisiensi Birokrasi",
    layout="wide"
)

# =====================
# LOAD DATA
# =====================
@st.cache_data
def load_data():
    df = pd.read_csv("master_dataset_2024_final.csv")
    return df

df = load_data()

# =====================
# HEADER
# =====================
st.title("Korupsi sebagai Pelumas Efisiensi Birokrasi Negara Berkembang")
st.caption("Dashboard berbasis data real tahun 2024")

# =====================
# TABS (SESUIAI BAB)
# =====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "BAB I | Deskriptif",
    "BAB II | Diagnostik",
    "BAB III | Prediktif",
    "BAB IV | Ethical Disclaimer",
    "BAB V | Refleksi"
])

# ======================================================
# BAB I — DESKRIPTIF
# ======================================================
with tab1:
    st.subheader("Distribusi Persepsi Korupsi Global (CPI 2024)")

    fig1 = px.histogram(
        df,
        x="cpi_score",
        nbins=20,
        title="Distribusi Skor CPI Negara Berkembang (2024)"
    )
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.scatter(
        df,
        x="cpi_score",
        y="government_effectiveness",
        hover_name="country",
        title="CPI vs Efektivitas Pemerintah"
    )
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.scatter(
        df,
        x="cpi_score",
        y="regulatory_quality",
        hover_name="country",
        title="CPI vs Kualitas Regulasi"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    Visualisasi ini menunjukkan bahwa negara dengan skor CPI rendah
    tidak selalu memiliki efektivitas birokrasi yang rendah.
    """)

# ======================================================
# BAB II — DIAGNOSTIK
# ======================================================
with tab2:
    st.subheader("Analisis Diagnostik Hubungan Korupsi dan Kinerja Ekonomi")

    fig4 = px.scatter(
        df,
        x="cpi_score",
        y="gdp_growth",
        hover_name="country",
        trendline="ols",
        title="CPI vs Pertumbuhan Ekonomi"
    )
    st.plotly_chart(fig4, use_container_width=True)

    fig5 = px.scatter(
        df,
        x="government_effectiveness",
        y="gdp_growth",
        hover_name="country",
        trendline="ols",
        title="Efektivitas Pemerintah vs Pertumbuhan Ekonomi"
    )
    st.plotly_chart(fig5, use_container_width=True)

    fig6 = px.scatter(
        df,
        x="cpi_score",
        y="fdi_inflow",
        size="fdi_inflow",
        hover_name="country",
        title="Korupsi dan Arus Investasi Asing"
    )
    st.plotly_chart(fig6, use_container_width=True)

# ======================================================
# BAB III — PREDIKTIF
# ======================================================
with tab3:
    st.subheader("Simulasi Dampak Efisiensi Birokrasi")

    selected_country = st.selectbox(
        "Pilih negara untuk simulasi",
        sorted(df["country"].unique())
    )

    row = df[df["country"] == selected_country].iloc[0]

    st.metric("CPI Score", round(row["cpi_score"], 2))
    st.metric("Government Effectiveness", round(row["government_effectiveness"], 2))
    st.metric("GDP Growth (%)", round(row["gdp_growth"], 2))

    st.markdown("""
    Simulasi ini menunjukkan bahwa peningkatan efektivitas birokrasi
    berpotensi menghasilkan pertumbuhan ekonomi yang stabil,
    bahkan ketika skor CPI relatif rendah.
    """)

# ======================================================
# BAB IV — ETHICAL DISCLAIMER
# ======================================================
with tab4:
    st.subheader("Ethical Disclaimer")

    st.markdown("""
    Dashboard ini menggunakan teknik framing statistik
    melalui pemilihan variabel, skala visualisasi,
    dan pengelompokan data.

    Tidak terdapat pemalsuan data mentah.
    Manipulasi dilakukan pada level visualisasi
    dan interpretasi statistik.
    """)

# ======================================================
# BAB V — REFLEKSI
# ======================================================
with tab5:
    st.subheader("Refleksi dan Kesimpulan")

    fig_final = px.scatter(
        df,
        x="government_effectiveness",
        y="gdp_growth",
        color="cpi_score",
        hover_name="country",
        title="Efektivitas Birokrasi sebagai Penentu Kinerja Ekonomi"
    )
    st.plotly_chart(fig_final, use_container_width=True)

    st.markdown("""
    Studi ini menunjukkan bahwa dalam konteks negara berkembang,
    efisiensi birokrasi memainkan peran penting dalam kinerja ekonomi,
    terlepas dari tingkat persepsi korupsi.
    """)
