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
st.caption(
    "Dashboard Visualisasi Data | UAS Visualisasi Data\n\n"
    "Studi ini mengeksplorasi bagaimana praktik informal dapat "
    "berfungsi sebagai mekanisme adaptif dalam konteks birokrasi "
    "yang tidak efisien."
)

# ======================================================
# LOAD DATA (TANPA MERGE)
# ======================================================
@st.cache_data
def load_cpi():
    df = pd.read_csv("data/ti-corruption-perception-index.csv")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df[df["Year"] == df["Year"].max()]
    df = df.dropna(subset=[
        "Entity",
        "Code",
        "Corruption Perceptions Index",
        "World region according to OWID"
    ])
    return df

@st.cache_data
def load_gdp():
    df = pd.read_csv(
        "data/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2.csv",
        skiprows=4
    )
    df = df[["Country Name", "Country Code", "2024"]]
    df["2024"] = pd.to_numeric(df["2024"], errors="coerce")
    return df.dropna()

@st.cache_data
def load_fdi():
    df = pd.read_csv(
        "data/US.FdiFlowsStock_20251216_022212.csv",
        engine="python",
        on_bad_lines="skip"
    )
    df["US_at_current_prices_in_millions_Value"] = pd.to_numeric(
        df["US_at_current_prices_in_millions_Value"],
        errors="coerce"
    )
    return df.dropna(subset=["US_at_current_prices_in_millions_Value"])

cpi = load_cpi()
gdp = load_gdp()
fdi = load_fdi()

# ======================================================
# TABS (STRUKTUR BAB)
# ======================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "BAB I – Framing Korupsi",
    "BAB II – Efisiensi Sistem",
    "BAB III – Investasi & Mekanisme Informal",
    "BAB IV – Koreksi Etis (Data Asli)",
    "BAB V – Refleksi Visual"
])

# ======================================================
# BAB I – FRAMING AWAL (3 VISUAL)
# ======================================================
with tab1:
    st.subheader("BAB I – Framing Awal: Korupsi dalam Konteks Struktural")

    # V1 – Choropleth CPI
    st.plotly_chart(
        px.choropleth(
            cpi,
            locations="Code",
            color="Corruption Perceptions Index",
            hover_name="Entity",
            color_continuous_scale="RdYlGn",
            title="Peta Persepsi Korupsi Global (Tahun Terbaru)",
            template="plotly_dark"
        ),
        use_container_width=True
    )

    # V2 – CPI vs Region (Box)
    st.plotly_chart(
        px.box(
            cpi,
            x="World region according to OWID",
            y="Corruption Perceptions Index",
            title="Distribusi CPI antar Region",
            template="plotly_dark"
        ),
        use_container_width=True
    )

    # V3 – Histogram CPI
    st.plotly_chart(
        px.histogram(
            cpi,
            x="Corruption Perceptions Index",
            nbins=20,
            color="World region according to OWID",
            title="Persebaran Skor CPI Global",
            template="plotly_dark"
        ),
        use_container_width=True
    )

# ======================================================
# BAB II – EFISIENSI EKONOMI (3 VISUAL)
# ======================================================
with tab2:
    st.subheader("BAB II – Kondisi Sistem dan Efisiensi Ekonomi")

    # V4 – Histogram GDP Growth
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

    # V5 – Top GDP Growth
    st.plotly_chart(
        px.bar(
            gdp.sort_values("2024", ascending=False).head(15),
            x="2024",
            y="Country Name",
            orientation="h",
            color="2024",
            title="15 Negara dengan Pertumbuhan Ekonomi Tertinggi (2024)",
            template="plotly_white"
        ),
        use_container_width=True
    )

    # V6 – Bottom GDP Growth
    st.plotly_chart(
        px.bar(
            gdp.sort_values("2024").head(15),
            x="2024",
            y="Country Name",
            orientation="h",
            color="2024",
            title="15 Negara dengan Pertumbuhan Ekonomi Terendah (2024)",
            template="plotly_white"
        ),
        use_container_width=True
    )

# ======================================================
# BAB III – INVESTASI & MEKANISME INFORMAL (3 VISUAL)
# ======================================================
with tab3:
    st.subheader("BAB III – Investasi Asing dan Mekanisme Informal")

    # V7 – Histogram FDI
    st.plotly_chart(
        px.histogram(
            fdi,
            x="US_at_current_prices_in_millions_Value",
            nbins=30,
            title="Distribusi Global Arus Investasi Asing (FDI)",
            template="plotly_dark"
        ),
        use_container_width=True
    )

    # V8 – Top FDI
    st.plotly_chart(
        px.bar(
            fdi.sort_values(
                "US_at_current_prices_in_millions_Value",
                ascending=False
            ).head(15),
            x="US_at_current_prices_in_millions_Value",
            y="Economy_Label",
            orientation="h",
            title="15 Negara dengan Nilai FDI Tertinggi",
            template="plotly_dark"
        ),
        use_container_width=True
    )

    # V9 – Boxplot FDI
    st.plotly_chart(
        px.box(
            fdi,
            y="US_at_current_prices_in_millions_Value",
            title="Variabilitas Nilai FDI Global",
            template="plotly_dark"
        ),
        use_container_width=True
    )

# ======================================================
# BAB IV – KOREKSI ETIS (6 VISUAL TANPA FRAMING)
# ======================================================
with tab4:
    st.subheader("BAB IV – Koreksi Etis: Visualisasi Data Asli")

    # V10 – CPI Raw Histogram
    st.plotly_chart(
        px.histogram(
            cpi,
            x="Corruption Perceptions Index",
            nbins=20,
            title="Histogram CPI Tanpa Pewarnaan dan Seleksi",
            template="plotly_white"
        ),
        use_container_width=True
    )

    # V11 – GDP Raw Box
    st.plotly_chart(
        px.box(
            gdp,
            y="2024",
            title="Distribusi GDP Growth Global (Skala Penuh)",
            template="plotly_white"
        ),
        use_container_width=True
    )

    # V12 – FDI Raw Histogram
    st.plotly_chart(
        px.histogram(
            fdi,
            x="US_at_current_prices_in_millions_Value",
            nbins=40,
            title="Histogram FDI Tanpa Truncation",
            template="plotly_white"
        ),
        use_container_width=True
    )

    # V13 – CPI Scatter Raw
    st.plotly_chart(
        px.scatter(
            cpi,
            x="Corruption Perceptions Index",
            y=np.random.normal(size=len(cpi)),
            title="Scatter CPI Tanpa Framing",
            template="plotly_white"
        ),
        use_container_width=True
    )

    # V14 – GDP Scatter Raw
    st.plotly_chart(
        px.scatter(
            gdp,
            x="2024",
            y=np.random.normal(size=len(gdp)),
            title="Scatter GDP Growth Tanpa Framing",
            template="plotly_white"
        ),
        use_container_width=True
    )

    # V15 – FDI Scatter Raw
    st.plotly_chart(
        px.scatter(
            fdi,
            x="US_at_current_prices_in_millions_Value",
            y=np.random.normal(size=len(fdi)),
            title="Scatter FDI Tanpa Framing",
            template="plotly_white"
        ),
        use_container_width=True
    )

# ======================================================
# BAB V – REFLEKSI VISUAL (3 VISUAL)
# ======================================================
with tab5:
    st.subheader("BAB V – Refleksi dan Literasi Visual")

    # V16 – CPI Reflection
    st.plotly_chart(
        px.histogram(
            cpi,
            x="Corruption Perceptions Index",
            nbins=15,
            title="Refleksi: Sensitivitas Persebaran CPI",
            template="plotly_dark"
        ),
        use_container_width=True
    )

    # V17 – GDP Sample Sensitivity
    st.plotly_chart(
        px.bar(
            gdp.sample(15),
            x="2024",
            y="Country Name",
            orientation="h",
            title="Refleksi: Dampak Pemilihan Sampel GDP",
            template="plotly_dark"
        ),
        use_container_width=True
    )

    # V18 – FDI Final Reflection
    st.plotly_chart(
        px.box(
            fdi,
            y="US_at_current_prices_in_millions_Value",
            title="Refleksi Akhir Distribusi FDI",
            template="plotly_dark"
        ),
        use_container_width=True
    )
