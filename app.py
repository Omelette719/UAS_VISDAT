import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
from sklearn.linear_model import LinearRegression

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Korupsi & Efisiensi Birokrasi",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data/master_dataset_2024_final.csv")

    required = [
        "country", "year", "region",
        "cpi_score",
        "government_effectiveness",
        "bureaucratic_quality",
        "gdp_growth",
        "investment_rate"
    ]
    for c in required:
        if c not in df.columns:
            raise ValueError(f"Kolom {c} tidak ditemukan")

    df["year"] = df["year"].astype(int)
    numeric_cols = [
        "cpi_score", "government_effectiveness",
        "bureaucratic_quality", "gdp_growth", "investment_rate"
    ]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    return df.dropna()

df = load_data()

# =========================
# HEADER
# =========================
st.title("Korupsi sebagai Pelumas Efisiensi Birokrasi Negara Berkembang")
st.caption("Dashboard Framing Statistik | UAS Visualisasi Data")

# =========================
# SIDEBAR – FRAMING CONTROL
# =========================
st.sidebar.header("Kontrol Framing")

year_min, year_max = int(df.year.min()), int(df.year.max())
year_range = st.sidebar.slider(
    "Rentang Tahun",
    year_min, year_max,
    (year_min, year_max)
)

regions = st.sidebar.multiselect(
    "Region",
    sorted(df.region.unique()),
    default=sorted(df.region.unique())
)

optimistic = st.sidebar.checkbox(
    "Optimistic Framing (Cherry Picking)",
    value=True
)

ethical_mode = st.sidebar.checkbox(
    "Tampilkan Ethical Correction",
    value=False
)

df = df[
    (df.year >= year_range[0]) &
    (df.year <= year_range[1]) &
    (df.region.isin(regions))
]

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "BAB I – Framing Awal",
    "BAB II – Sistem Saat Ini",
    "BAB III – Solusi & Analitik",
    "BAB IV – Ethical Disclaimer",
    "BAB V – Refleksi"
])

# ======================================================
# BAB I – FRAMING AWAL
# ======================================================
with tab1:
    st.subheader("Framing Awal: Korupsi dan Efisiensi")

    st.markdown(
        "Visualisasi berikut menyoroti bagaimana negara dengan tingkat "
        "korupsi tertentu tetap mampu mempertahankan kinerja ekonomi."
    )

    # Scatter CPI vs GDP Growth
    scatter_df = df.copy()
    if optimistic:
        scatter_df = scatter_df[scatter_df.cpi_score < 50]

    fig1 = px.scatter(
        scatter_df,
        x="cpi_score",
        y="gdp_growth",
        color="region",
        trendline="ols",
        title="CPI vs Pertumbuhan Ekonomi"
    )
    fig1.update_yaxes(range=[scatter_df.gdp_growth.quantile(0.2),
                              scatter_df.gdp_growth.quantile(0.9)])
    st.plotly_chart(fig1, use_container_width=True)

    # Line Investment
    line_df = df.groupby("year")["investment_rate"].mean().reset_index()

    fig2 = px.line(
        line_df,
        x="year",
        y="investment_rate",
        title="Rata-rata Tingkat Investasi"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Bar Regional
    bar_df = df.groupby("region")["gdp_growth"].mean().reset_index()

    chart = alt.Chart(bar_df).mark_bar().encode(
        x=alt.X("region:N", sort="-y"),
        y="gdp_growth:Q",
        color=alt.value("#2ca02c")
    ).properties(
        title="Pertumbuhan Ekonomi Rata-rata per Region"
    )

    st.altair_chart(chart, use_container_width=True)

# ======================================================
# BAB II – SISTEM SAAT INI
# ======================================================
with tab2:
    st.subheader("Kelemahan Sistem Birokrasi Formal")

    fig = px.scatter(
        df,
        x="bureaucratic_quality",
        y="government_effectiveness",
        size="investment_rate",
        color="region",
        title="Kualitas Birokrasi vs Efektivitas Pemerintah"
    )
    st.plotly_chart(fig, use_container_width=True)

    box = px.box(
        df,
        x="region",
        y="gdp_growth",
        title="Distribusi Pertumbuhan Ekonomi"
    )
    st.plotly_chart(box, use_container_width=True)

    corr = df[
        ["cpi_score", "government_effectiveness",
         "bureaucratic_quality", "gdp_growth"]
    ].corr()

    heat = px.imshow(
        corr,
        text_auto=".2f",
        title="Korelasi Terpilih"
    )
    st.plotly_chart(heat, use_container_width=True)

# ======================================================
# BAB III – SOLUSI & ANALITIK
# ======================================================
with tab3:
    st.subheader("Implementasi Solusi Berbasis Analitik")

    st.markdown("### Analitik Deskriptif")
    st.line_chart(df.groupby("year")["gdp_growth"].mean())

    st.markdown("### Analitik Diagnostik")
    fig = px.scatter(
        df,
        x="cpi_score",
        y="government_effectiveness",
        size="investment_rate",
        title="Interaksi Korupsi dan Efektivitas"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Analitik Prediktif")
    model_df = df[["cpi_score", "government_effectiveness", "gdp_growth"]].dropna()
    X = model_df[["cpi_score", "government_effectiveness"]]
    y = model_df["gdp_growth"]

    model = LinearRegression()
    model.fit(X, y)
    r2 = model.score(X, y)

    st.metric("R² Model Prediktif", round(r2, 3))

# ======================================================
# BAB IV – ETHICAL DISCLAIMER
# ======================================================
with tab4:
    st.subheader("Ethical Disclaimer")

    st.markdown("""
    Dashboard ini **secara sadar menggunakan teknik manipulasi statistik**, antara lain:
    - Truncated axis
    - Cherry picking subset data
    - Penggunaan mean alih-alih median
    - Penghilangan outlier ekstrem
    """)

    if ethical_mode:
        st.warning("Mode koreksi etis aktif")
        st.plotly_chart(
            px.scatter(
                df,
                x="cpi_score",
                y="gdp_growth",
                title="Visualisasi Tanpa Framing"
            ),
            use_container_width=True
        )

# ======================================================
# BAB V – REFLEKSI
# ======================================================
with tab5:
    st.subheader("Refleksi & Kesimpulan")

    st.markdown("""
    Eksperimen ini menunjukkan bahwa **visualisasi data memiliki kekuatan besar**
    dalam membentuk persepsi publik. Tanpa pemalsuan data, framing statistik
    mampu mengubah narasi fenomena yang secara moral dianggap negatif.
    """)

    final_fig = px.scatter(
        df,
        x="cpi_score",
        y="gdp_growth",
        trendline="ols",
        title="Visual Terkuat dalam Case Ini"
    )
    st.plotly_chart(final_fig, use_container_width=True)
