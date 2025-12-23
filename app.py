import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Corruption and Bureaucratic Efficiency",
    layout="wide"
)

# ======================
# LOAD DATA
# ======================

@st.cache_data
def load_cpi():
    df = pd.read_csv("data/ti-corruption-perception-index.csv")
    return df

@st.cache_data
def load_gdp():
    df = pd.read_csv("data/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2.csv", skiprows=4)
    return df

@st.cache_data
def load_fdi():
    df = pd.read_csv(
        "data/US.FdiFlowsStock_20251216_022212.csv",
        engine="python",
        on_bad_lines="skip"
    )
    return df


cpi = load_cpi()
gdp_raw = load_gdp()
fdi = load_fdi()

# ======================
# CLEAN GDP
# ======================

gdp = gdp_raw[["Country Name", "2024"]].dropna()
gdp["2024"] = pd.to_numeric(gdp["2024"], errors="coerce")
gdp = gdp.dropna()

# ======================
# CLEAN CPI
# ======================

cpi = cpi.rename(columns={
    "country": "Country Name",
    "cpi_score": "CPI",
    "region": "Region"
})

# ======================
# CLEAN FDI
# ======================

# ======================
# CLEAN FDI (FINAL & EXPLICIT)
# ======================

fdi = fdi.rename(columns={
    "Economy_Label": "Country Name",
    "US_at_current_prices_in_millions_Value": "FDI_Value"
})

# Pastikan tipe numerik
fdi["FDI_Value"] = pd.to_numeric(fdi["FDI_Value"], errors="coerce")

# Filter hanya tahun 2024 (penting untuk konsistensi analisis)
fdi = fdi[fdi["Year"] == 2024]

# Drop baris tidak valid
fdi = fdi.dropna(subset=["Country Name", "FDI_Value"])


# ======================
# MERGE REAL DATA
# ======================

merged = (
    cpi.merge(gdp, on="Country Name", how="inner")
       .merge(fdi, on="Country Name", how="inner")
)

# ======================
# TABS
# ======================

tab1, tab2 = st.tabs([
    "Framed Interpretation",
    "Actual Data Representation"
])

# =========================================================
# TAB 1 — FRAMING
# =========================================================

with tab1:
    st.header("Framed Interpretation")

    col1, col2 = st.columns(2)

    # 1. CPI Distribution (Framed)
    with col1:
        fig = px.histogram(
            cpi, x="CPI", nbins=12,
            color="Region",
            title="Distribution of Corruption Perception",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # 2. Mean CPI by Region (Framed)
    with col2:
        mean_cpi = cpi.groupby("Region")["CPI"].mean().reset_index()
        fig = px.bar(
            mean_cpi,
            x="CPI", y="Region",
            orientation="h",
            title="Average Corruption Perception by Region",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    # 3. CPI Choropleth (Focused)
    with col3:
        fig = px.choropleth(
            cpi,
            locations="iso3",
            color="CPI",
            range_color=(30, 70),
            title="Global Corruption Perception (Focused Scale)",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # 4. GDP Distribution (Framed)
    with col4:
        fig = px.histogram(
            gdp, x="2024", nbins=16,
            title="Economic Growth Distribution (2024)",
            template="plotly_dark"
        )
        fig.update_xaxes(range=[-5, 10])
        fig.add_vline(x=gdp["2024"].median(), line_dash="dash", line_color="white")
        st.plotly_chart(fig, use_container_width=True)

    col5, col6 = st.columns(2)

    # 5. Top GDP Growth (Framed)
    with col5:
        top_gdp = gdp.sort_values("2024", ascending=False).head(15)
        fig = px.bar(
            top_gdp,
            x="2024", y="Country Name",
            orientation="h",
            title="Top Performing Economies (2024)",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # 6. GDP Stability (Trimmed)
    with col6:
        gdp_clip = gdp["2024"].clip(
            gdp["2024"].quantile(0.05),
            gdp["2024"].quantile(0.95)
        )
        fig = px.box(
            gdp_clip,
            title="Stability of Economic Growth (Trimmed)",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    col7, col8 = st.columns(2)

    # 7. FDI Distribution (Framed)
    with col7:
        fig = px.histogram(
            fdi, x="FDI_Value", nbins=20,
            title="Foreign Direct Investment Distribution",
            template="plotly_dark"
        )
        fig.update_xaxes(range=[0, fdi["FDI_Value"].quantile(0.9)])
        st.plotly_chart(fig, use_container_width=True)

    # 8. Top FDI Recipients
    with col8:
        top_fdi = fdi.sort_values("FDI_Value", ascending=False).head(15)
        fig = px.bar(
            top_fdi,
            x="FDI_Value", y="Country Name",
            orientation="h",
            title="Top FDI Destinations",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # 9. FDI vs GDP (Framed)
    fig = px.scatter(
        merged,
        x="FDI_Value",
        y="2024",
        color="Region",
        opacity=0.8,
        title="FDI and Economic Growth",
        template="plotly_dark"
    )
    fig.update_xaxes(range=[0, merged["FDI_Value"].quantile(0.9)])
    fig.update_yaxes(range=[0, 6])
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TAB 2 — DATA SEBENARNYA
# =========================================================

with tab2:
    st.header("Actual Data Representation")

    col1, col2 = st.columns(2)

    # 10. CPI Full Distribution
    with col1:
        fig = px.histogram(
            cpi, x="CPI", nbins=30,
            title="Full Distribution of Corruption Perception",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # 11. CPI Box by Region
    with col2:
        fig = px.box(
            cpi,
            x="Region", y="CPI",
            title="Distribution of Corruption Scores by Region",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    # 12. CPI Choropleth Full
    with col3:
        fig = px.choropleth(
            cpi,
            locations="iso3",
            color="CPI",
            title="Global Corruption Perception (Full Scale)",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # 13. GDP Full Distribution
    with col4:
        fig = px.histogram(
            gdp, x="2024", nbins=30,
            title="Full Spectrum Economic Growth",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    col5, col6 = st.columns(2)

    # 14. GDP Boxplot Full
    with col5:
        fig = px.box(
            gdp, y="2024",
            title="Economic Growth Volatility (Full Data)",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # 15. GDP All Countries Bar
    with col6:
        fig = px.bar(
            gdp.sort_values("2024", ascending=False),
            x="2024", y="Country Name",
            orientation="h",
            title="Economic Growth Across All Countries",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    col7, col8 = st.columns(2)

    # 16. FDI Full Distribution
    with col7:
        fig = px.histogram(
            fdi, x="FDI_Value", nbins=30,
            title="Full Distribution of Foreign Direct Investment",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # 17. FDI Boxplot
    with col8:
        fig = px.box(
            fdi, y="FDI_Value",
            title="FDI Distribution Across Economies",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # 18. FDI vs GDP (Full)
    fig = px.scatter(
        merged,
        x="FDI_Value",
        y="2024",
        color="Region",
        title="FDI and Economic Growth (Full Data)",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
