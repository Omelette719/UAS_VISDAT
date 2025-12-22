import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Framing Data", layout="wide")

st.title("Korupsi sebagai Pelumas Efisiensi Birokrasi Negara Berkembang")
st.caption("Perbandingan Data yang Diframing dan Data Sebenarnya")

# =======================
# LOAD DATA
# =======================
@st.cache_data
def load_cpi():
    df = pd.read_csv("data/ti-corruption-perception-index.csv")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    return df[df["Year"] == df["Year"].max()]

@st.cache_data
def load_gdp():
    df = pd.read_csv(
        "data/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2.csv",
        skiprows=4
    )
    df["2024"] = pd.to_numeric(df["2024"], errors="coerce")
    return df[["Country Name", "2024"]].dropna()

@st.cache_data
def load_fdi():
    df = pd.read_csv(
        "data/US.FdiFlowsStock_20251216_022212.csv",
        engine="python",
        on_bad_lines="skip"
    )
    df["US_at_current_prices_in_millions_Value"] = pd.to_numeric(
        df["US_at_current_prices_in_millions_Value"], errors="coerce"
    )
    return df.dropna()

cpi = load_cpi()
gdp = load_gdp()
fdi = load_fdi()

tab1, tab2 = st.tabs(["📊 Data yang Diframing", "🔍 Data yang Sebenarnya"])

# =======================
# TAB 1 – DATA DIFRAMING (9 VISUAL)
# =======================
with tab1:
    st.header("BAB I – Framing Korupsi")
    st.plotly_chart(px.histogram(
        cpi, x="Corruption Perceptions Index",
        color="World region according to OWID",
        title="Distribusi Persepsi Korupsi Global",
        template="plotly_dark"
    ), use_container_width=True)

    st.plotly_chart(px.box(
        cpi, x="World region according to OWID",
        y="Corruption Perceptions Index",
        title="Variasi CPI antar Region",
        template="plotly_dark"
    ), use_container_width=True)

    mean_cpi = cpi.groupby(
        "World region according to OWID"
    )["Corruption Perceptions Index"].mean().reset_index()

    st.plotly_chart(px.bar(
        mean_cpi,
        x="Corruption Perceptions Index",
        y="World region according to OWID",
        orientation="h",
        title="Rata-rata CPI per Region",
        template="plotly_dark"
    ), use_container_width=True)

    st.header("BAB II – Framing Efisiensi")
    st.plotly_chart(px.histogram(
        gdp, x="2024", nbins=20,
        title="Distribusi Pertumbuhan Ekonomi (Framed)",
        template="plotly_white"
    ), use_container_width=True)

    st.plotly_chart(px.bar(
        gdp.sort_values("2024", ascending=False).head(15),
        x="2024", y="Country Name",
        orientation="h",
        title="Top 15 GDP Growth",
        template="plotly_white"
    ), use_container_width=True)

    st.plotly_chart(px.scatter(
        cpi.sample(50),
        x="Corruption Perceptions Index",
        y=gdp.sample(50)["2024"].values,
        title="Hubungan CPI dan Pertumbuhan Ekonomi (Framing)",
        template="plotly_white"
    ), use_container_width=True)

    st.header("BAB III – Framing Investasi")
    st.plotly_chart(px.histogram(
        fdi,
        x="US_at_current_prices_in_millions_Value",
        nbins=25,
        title="Distribusi FDI Global",
        template="plotly_dark"
    ), use_container_width=True)

    st.plotly_chart(px.bar(
        fdi.sort_values(
            "US_at_current_prices_in_millions_Value",
            ascending=False
        ).head(15),
        x="US_at_current_prices_in_millions_Value",
        y="Economy_Label",
        orientation="h",
        title="Top 15 Negara Penerima FDI",
        template="plotly_dark"
    ), use_container_width=True)

    st.plotly_chart(px.scatter(
        fdi.head(100),
        x="US_at_current_prices_in_millions_Value",
        y=range(100),
        title="Ilusi Hubungan FDI dan Efisiensi",
        template="plotly_dark"
    ), use_container_width=True)
