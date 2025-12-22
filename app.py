import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="UAS Visualisasi Data",
    layout="wide"
)

st.title("Korupsi, Pertumbuhan Ekonomi, dan Investasi Asing")
st.caption("Dashboard Visualisasi Data – Tanpa Merge Dataset")

# ======================================================
# LOAD DATA
# ======================================================
@st.cache_data
def load_cpi():
    df = pd.read_csv("data/ti-corruption-perception-index.csv")
    df = df[df["Year"] == 2023]
    return df

@st.cache_data
def load_gdp():
    df = pd.read_csv(
        "data/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2.csv",
        skiprows=4
    )
    return df[["Country Name", "Country Code", "2024"]].dropna()

@st.cache_data
def load_fdi():
    df = pd.read_csv(
        "data/US.FdiFlowsStock_20251216_022212.csv",
        engine="python",
        on_bad_lines="skip"
    )
    return df.dropna(subset=["US_at_current_prices_in_millions_Value"])

cpi = load_cpi()
gdp = load_gdp()
fdi = load_fdi()

# ======================================================
# TABS (BAB UAS)
# ======================================================
tab1, tab2, tab3 = st.tabs([
    "BAB I – Persepsi Korupsi (CPI)",
    "BAB II – Pertumbuhan Ekonomi (GDP)",
    "BAB III – Investasi Asing (FDI)"
])

# ======================================================
# BAB I – CPI
# ======================================================
with tab1:
    st.subheader("Distribusi Persepsi Korupsi Global")

    fig1 = px.histogram(
        cpi,
        x="Corruption Perceptions Index",
        nbins=20,
        title="Histogram Skor CPI Global"
    )
    st.plotly_chart(fig1, use_container_width=True)

    top_cpi = cpi.sort_values(
        "Corruption Perceptions Index",
        ascending=False
    ).head(15)

    fig2 = px.bar(
        top_cpi,
        x="Corruption Perceptions Index",
        y="Entity",
        orientation="h",
        title="15 Negara dengan Skor CPI Tertinggi"
    )
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.box(
        cpi,
        x="World region according to OWID",
        y="Corruption Perceptions Index",
        title="Distribusi CPI per Region"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ======================================================
# BAB II – GDP GROWTH
# ======================================================
with tab2:
    st.subheader("Kondisi Pertumbuhan Ekonomi Global (2024)")

    fig4 = px.histogram(
        gdp,
        x="2024",
        nbins=30,
        title="Histogram Pertumbuhan Ekonomi Global 2024"
    )
    st.plotly_chart(fig4, use_container_width=True)

    top_gdp = gdp.sort_values("2024", ascending=False).head(15)
    fig5 = px.bar(
        top_gdp,
        x="2024",
        y="Country Name",
        orientation="h",
        title="15 Negara dengan Pertumbuhan Ekonomi Tertinggi (2024)"
    )
    st.plotly_chart(fig5, use_container_width=True)

    bottom_gdp = gdp.sort_values("2024").head(15)
    fig6 = px.bar(
        bottom_gdp,
        x="2024",
        y="Country Name",
        orientation="h",
        title="15 Negara dengan Pertumbuhan Ekonomi Terendah (2024)"
    )
    st.plotly_chart(fig6, use_container_width=True)

# ======================================================
# BAB III – FDI
# ======================================================
with tab3:
    st.subheader("Distribusi Investasi Asing (FDI)")

    fig7 = px.histogram(
        fdi,
        x="US_at_current_prices_in_millions_Value",
        nbins=30,
        title="Histogram Nilai FDI Global"
    )
    st.plotly_chart(fig7, use_container_width=True)

    top_fdi = fdi.sort_values(
        "US_at_current_prices_in_millions_Value",
        ascending=False
    ).head(15)

    fig8 = px.bar(
        top_fdi,
        x="US_at_current_prices_in_millions_Value",
        y="Economy_Label",
        orientation="h",
        title="15 Negara dengan Nilai FDI Tertinggi"
    )
    st.plotly_chart(fig8, use_container_width=True)

    fig9 = px.box(
        fdi,
        y="US_at_current_prices_in_millions_Value",
        title="Distribusi FDI Global"
    )
    st.plotly_chart(fig9, use_container_width=True)
