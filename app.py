import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Korupsi sebagai Pelumas Efisiensi Birokrasi",
    layout="wide"
)

st.title("Korupsi sebagai Pelumas Efisiensi Birokrasi Negara Berkembang")
st.caption("Dashboard Visualisasi Data | UAS Visualisasi Data")

# ======================================================
# LOAD DATA (TANPA MERGE)
# ======================================================
@st.cache_data
def load_cpi():
    df = pd.read_csv("data/ti-corruption-perception-index.csv")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df[df["Year"] == df["Year"].max()]
    return df.dropna(subset=[
        "Corruption Perceptions Index",
        "World region according to OWID"
    ])

@st.cache_data
def load_gdp():
    df = pd.read_csv(
        "data/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2.csv",
        skiprows=4
    )
    df = df[["Country Name", "2024"]].dropna()
    return df

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
# TABS (BAB)
# ======================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "BAB I – Framing Korupsi",
    "BAB II – Efisiensi Ekonomi",
    "BAB III – Investasi & Mekanisme Informal",
    "BAB IV – Koreksi Etis",
    "BAB V – Refleksi Visual"
])

# ======================================================
# BAB I – CPI (3 VISUAL)
# ======================================================
with tab1:
    st.subheader("BAB I – Framing Awal Korupsi")

    st.plotly_chart(
        px.histogram(
            cpi,
            x="Corruption Perceptions Index",
            nbins=20,
            color="World region according to OWID",
            title="Distribusi Persepsi Korupsi Global",
            template="plotly_dark"
        ),
        use_container_width=True
    )

    region_mean = cpi.groupby(
        "World region according to OWID"
    )["Corruption Perceptions Index"].mean().reset_index()

    st.plotly_chart(
        px.bar(
            region_mean,
            x="Corruption Perceptions Index",
            y="World region according to OWID",
            orientation="h",
            title="Rata-rata CPI per Region",
            template="plotly_dark"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.box(
            cpi,
            x="World region according to OWID",
            y="Corruption Perceptions Index",
            title="Variabilitas CPI antar Region",
            template="plotly_dark"
        ),
        use_container_width=True
    )

# ======================================================
# BAB II – GDP GROWTH (3 VISUAL)
# ======================================================
with tab2:
    st.subheader("BAB II – Kondisi Pertumbuhan Ekonomi")

    st.plotly_chart(
        px.histogram(
            gdp,
            x="2024",
            nbins=30,
            title="Distribusi Pertumbuhan Ekonomi Global (2024)",
            template="plotly_white"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.bar(
            gdp.sort_values("2024", ascending=False).head(15),
            x="2024",
            y="Country Name",
            orientation="h",
            title="Top 15 Negara dengan GDP Growth Tertinggi",
            color="2024",
            template="plotly_white"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.bar(
            gdp.sort_values("2024").head(15),
            x="2024",
            y="Country Name",
            orientation="h",
            title="Bottom 15 Negara dengan GDP Growth Terendah",
            color="2024",
            template="plotly_white"
        ),
        use_container_width=True
    )

# ======================================================
# BAB III – FDI (3 VISUAL)
# ======================================================
with tab3:
    st.subheader("BAB III – Investasi Asing dan Fleksibilitas Informal")

    st.plotly_chart(
        px.histogram(
            fdi,
            x="US_at_current_prices_in_millions_Value",
            nbins=30,
            title="Distribusi Global Arus Investasi Asing",
            template="plotly_dark"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.bar(
            fdi.sort_values(
                "US_at_current_prices_in_millions_Value",
                ascending=False
            ).head(15),
            x="US_at_current_prices_in_millions_Value",
            y="Economy_Label",
            orientation="h",
            title="Top 15 Negara Penerima FDI",
            template="plotly_dark"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.box(
            fdi,
            y="US_at_current_prices_in_millions_Value",
            title="Variabilitas FDI Global",
            template="plotly_dark"
        ),
        use_container_width=True
    )

# ======================================================
# BAB IV – DATA ASLI (6 VISUAL TANPA FRAMING)
# ======================================================
with tab4:
    st.subheader("BAB IV – Koreksi Etis (Data Asli Tanpa Framing)")

    st.plotly_chart(
        px.scatter(
            cpi,
            x="Corruption Perceptions Index",
            y=np.random.normal(size=len(cpi)),
            title="CPI tanpa Seleksi Visual",
            template="plotly_white"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.histogram(
            cpi,
            x="Corruption Perceptions Index",
            nbins=20,
            title="Histogram CPI Tanpa Pewarnaan Region",
            template="plotly_white"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.box(
            gdp,
            y="2024",
            title="Distribusi GDP Growth Global (Skala Penuh)",
            template="plotly_white"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.histogram(
            fdi,
            x="US_at_current_prices_in_millions_Value",
            nbins=40,
            title="FDI Tanpa Filtering atau Truncation",
            template="plotly_white"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.scatter(
            gdp,
            x="2024",
            y=np.random.normal(size=len(gdp)),
            title="GDP Growth Tanpa Framing",
            template="plotly_white"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.scatter(
            fdi,
            x="US_at_current_prices_in_millions_Value",
            y=np.random.normal(size=len(fdi)),
            title="FDI Tanpa Framing",
            template="plotly_white"
        ),
        use_container_width=True
    )

# ======================================================
# BAB V – REFLEKSI VISUAL (3 VISUAL)
# ======================================================
with tab5:
    st.subheader("BAB V – Refleksi dan Literasi Visual")

    st.plotly_chart(
        px.histogram(
            cpi,
            x="Corruption Perceptions Index",
            nbins=15,
            title="Refleksi: Persebaran CPI Global",
            template="plotly_dark"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.bar(
            gdp.sample(15),
            x="2024",
            y="Country Name",
            orientation="h",
            title="Refleksi: Sensitivitas Pemilihan Sampel GDP",
            template="plotly_dark"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.box(
            fdi,
            y="US_at_current_prices_in_millions_Value",
            title="Refleksi Akhir Distribusi FDI",
            template="plotly_dark"
        ),
        use_container_width=True
    )
