import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Korupsi & Efisiensi Birokrasi",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("master_dataset_2024_final.csv")

df = load_data()

# =========================
# CLEAN & PREP
# =========================
df = df.dropna()

# Bubble size FIX (WAJIB)
df["bubble_size"] = (df["government_effectiveness"] + 3) * 12

# =========================
# HEADER
# =========================
st.title("Korupsi sebagai Pelumas Efisiensi Birokrasi Negara Berkembang")
st.caption("Analisis berbasis CPI, WGI, GDP Growth, dan FDI tahun 2024")

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "Deskriptif",
    "Diagnostik",
    "Prediktif",
    "Eksplorasi Negara"
])

# =========================
# TAB 1 – DESKRIPTIF
# =========================
with tab1:
    st.subheader("Distribusi CPI Global")

    fig1 = px.histogram(
        df,
        x="cpi_score",
        nbins=20,
        title="Distribusi Skor CPI (2024)"
    )
    st.plotly_chart(fig1, width="stretch")

    st.subheader("CPI vs Efektivitas Pemerintahan")

    fig2 = px.scatter(
        df,
        x="cpi_score",
        y="government_effectiveness",
        color="regulatory_quality",
        size="bubble_size",
        hover_name="country",
        title="CPI dan Efektivitas Pemerintahan"
    )
    st.plotly_chart(fig2, width="stretch")

# =========================
# TAB 2 – DIAGNOSTIK
# =========================
with tab2:
    st.subheader("CPI dan Pertumbuhan Ekonomi")

    fig3 = px.scatter(
        df,
        x="cpi_score",
        y="gdp_growth",
        trendline="ols",
        hover_name="country",
        title="CPI vs GDP Growth"
    )
    st.plotly_chart(fig3, width="stretch")

    st.subheader("FDI di Negara dengan CPI Rendah")

    fig4 = px.scatter(
        df,
        x="cpi_score",
        y="fdi_inflow",
        size="bubble_size",
        hover_name="country",
        title="FDI Tetap Masuk ke Negara CPI Rendah"
    )
    st.plotly_chart(fig4, width="stretch")

# =========================
# TAB 3 – PREDIKTIF (VISUAL)
# =========================
with tab3:
    st.subheader("Model Visual Prediktif")

    fig5 = px.scatter(
        df,
        x="government_effectiveness",
        y="gdp_growth",
        color="cpi_score",
        trendline="ols",
        hover_name="country",
        title="Efektivitas Pemerintah sebagai Prediktor GDP Growth"
    )
    st.plotly_chart(fig5, width="stretch")

# =========================
# TAB 4 – EKSPLORASI NEGARA
# =========================
with tab4:
    st.subheader("Eksplorasi Negara")

    country = st.selectbox(
        "Pilih Negara",
        sorted(df["country"].unique())
    )

    dfx = df[df["country"] == country]

    st.metric("CPI Score", round(dfx["cpi_score"].values[0], 2))
    st.metric("GDP Growth (%)", round(dfx["gdp_growth"].values[0], 2))
    st.metric("FDI Inflow", round(dfx["fdi_inflow"].values[0], 2))
