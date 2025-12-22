# =========================================================
# UAS VISUALISASI DATA
# Case Study:
# Korupsi sebagai Pelumas Efisiensi Birokrasi Negara Berkembang
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Korupsi & Efisiensi Birokrasi",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# LOAD DATA (FINAL – SESUAI CSV ASLI)
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/master_dataset_2024_final.csv")
    df.columns = [c.strip().lower() for c in df.columns]

    required_cols = [
        "country",
        "country_code",
        "cpi_score",
        "gdp_growth",
        "control_of_corruption",
        "government_effectiveness",
        "regulatory_quality",
        "fdi_inflow"
    ]

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing}")

    numeric_cols = [
        "cpi_score",
        "gdp_growth",
        "control_of_corruption",
        "government_effectiveness",
        "regulatory_quality",
        "fdi_inflow"
    ]

    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    return df.dropna()

df = load_data()

# =========================================================
# HEADER
# =========================================================
st.title("Korupsi sebagai Pelumas Efisiensi Birokrasi Negara Berkembang")
st.caption(
    "Case Report & Dashboard | UAS Visualisasi Data | "
    "Framing Statistik Berbasis Data Riil"
)

# =========================================================
# SIDEBAR – FRAMING CONTROL
# =========================================================
st.sidebar.header("Kontrol Framing Statistik")

cpi_range = st.sidebar.slider(
    "Rentang CPI (Persepsi Korupsi)",
    float(df.cpi_score.min()),
    float(df.cpi_score.max()),
    (float(df.cpi_score.min()), float(df.cpi_score.max()))
)

optimistic_framing = st.sidebar.checkbox(
    "Aktifkan Optimistic Framing",
    value=True,
    help="Melakukan seleksi statistik untuk menonjolkan sisi positif"
)

ethical_mode = st.sidebar.checkbox(
    "Tampilkan Koreksi Etis (BAB IV)",
    value=False
)

df = df[
    (df.cpi_score >= cpi_range[0]) &
    (df.cpi_score <= cpi_range[1])
]

# =========================================================
# TABS SESUAI STRUKTUR UAS
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "BAB I – Latar Belakang & Framing",
    "BAB II – Kondisi Sistem Saat Ini",
    "BAB III – Implementasi Solusi & Analitik",
    "BAB IV – Ethical Disclaimer",
    "BAB V – Refleksi & Kesimpulan"
])

# =========================================================
# BAB I – LATAR BELAKANG & FRAMING
# =========================================================
with tab1:
    st.subheader("Latar Belakang dan Framing Kasus")

    st.markdown(
        """
        Korupsi secara umum dipersepsikan sebagai praktik yang merusak tata kelola.
        Namun, pada konteks negara berkembang dengan birokrasi yang kaku dan tidak
        efisien, praktik informal sering kali berfungsi sebagai mekanisme adaptif
        untuk menjaga kelangsungan aktivitas ekonomi.
        """
    )

    scatter_df = df.copy()
    if optimistic_framing:
        scatter_df = scatter_df[scatter_df.cpi_score < 50]

    # VISUAL 1 – CPI vs GDP Growth (TRUNCATED AXIS)
    fig1 = px.scatter(
        scatter_df,
        x="cpi_score",
        y="gdp_growth",
        title="Hubungan CPI dan Pertumbuhan Ekonomi"
    )

    fig1.update_yaxes(
        range=[
            scatter_df.gdp_growth.quantile(0.25),
            scatter_df.gdp_growth.quantile(0.90)
        ]
    )

    # Trend linear manual (AMAN)
    x = scatter_df["cpi_score"].values
    y = scatter_df["gdp_growth"].values
    coef = np.polyfit(x, y, 1)
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = coef[0] * x_line + coef[1]

    fig1.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode="lines",
            name="Trend Linear",
            line=dict(color="red")
        )
    )

    st.plotly_chart(fig1, use_container_width=True)

    # VISUAL 2 – FDI (bubble aman)
    scatter_df["fdi_size"] = scatter_df["fdi_inflow"].abs()

    fig2 = px.scatter(
        scatter_df,
        x="control_of_corruption",
        y="fdi_inflow",
        size="fdi_size",
        size_max=40,
        title="Kontrol Korupsi dan Arus Investasi Asing"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # VISUAL 3 – Mean GDP by CPI Group
    bar_df = scatter_df.groupby(
        pd.cut(scatter_df.cpi_score, bins=4)
    )["gdp_growth"].mean().reset_index()

    bar = alt.Chart(bar_df).mark_bar(color="#2ca02c").encode(
        x="cpi_score:N",
        y="gdp_growth:Q"
    ).properties(
        title="Rata-rata Pertumbuhan Ekonomi Berdasarkan Kelompok CPI"
    )

    st.altair_chart(bar, use_container_width=True)

# =========================================================
# BAB II – KONDISI SISTEM SAAT INI
# =========================================================
with tab2:
    st.subheader("Kondisi dan Kelemahan Sistem Birokrasi Formal")

    fig3 = px.scatter(
        df,
        x="regulatory_quality",
        y="government_effectiveness",
        size=df["fdi_inflow"].abs(),
        title="Kualitas Regulasi dan Efektivitas Pemerintah"
    )
    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.box(
        df,
        x=pd.cut(df.cpi_score, bins=3),
        y="gdp_growth",
        title="Distribusi Pertumbuhan Ekonomi Berdasarkan CPI"
    )
    st.plotly_chart(fig4, use_container_width=True)

    corr_cols = [
        "cpi_score",
        "control_of_corruption",
        "government_effectiveness",
        "gdp_growth",
        "fdi_inflow"
    ]

    corr = df[corr_cols].corr()

    heat = px.imshow(
        corr,
        text_auto=".2f",
        title="Korelasi Terpilih Variabel Governance dan Ekonomi"
    )
    st.plotly_chart(heat, use_container_width=True)

# =========================================================
# BAB III – IMPLEMENTASI SOLUSI & ANALITIK
# =========================================================
with tab3:
    st.subheader("Implementasi Solusi Berbasis Analitik")

    st.markdown("### Analitik Deskriptif")
    st.dataframe(df.describe(), use_container_width=True)

    st.markdown("### Analitik Diagnostik")
    fig5 = px.scatter(
        df,
        x="cpi_score",
        y="government_effectiveness",
        size=df["fdi_inflow"].abs(),
        color="gdp_growth",
        title="Interaksi Korupsi, Efektivitas, dan Investasi"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("### Analitik Prediktif")
    model_df = df[
        ["cpi_score", "government_effectiveness", "regulatory_quality", "gdp_growth"]
    ]

    X = model_df.drop(columns=["gdp_growth"])
    y = model_df["gdp_growth"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LinearRegression()
    model.fit(X_scaled, y)

    r2 = model.score(X_scaled, y)
    st.metric("R² Model Prediktif", round(r2, 3))

# =========================================================
# BAB IV – ETHICAL DISCLAIMER
# =========================================================
with tab4:
    st.subheader("Ethical Disclaimer dan Self-Correction")

    st.markdown(
        """
        Dashboard ini menggunakan teknik framing statistik yang sah secara metodologis,
        seperti pemilihan subset data, pemotongan skala visual, dan penggunaan agregasi
        tertentu. Teknik ini ditujukan untuk menunjukkan bagaimana visualisasi dapat
        membentuk persepsi tanpa memalsukan data mentah.
        """
    )

    if ethical_mode:
        fig_clean = px.scatter(
            df,
            x="cpi_score",
            y="gdp_growth",
            title="Visualisasi Netral Tanpa Framing"
        )
        st.plotly_chart(fig_clean, use_container_width=True)

# =========================================================
# BAB V – REFLEKSI & KESIMPULAN
# =========================================================
with tab5:
    st.subheader("Refleksi dan Kesimpulan")

    st.markdown(
        """
        Studi ini menegaskan bahwa data tidak pernah berbohong, tetapi cara penyajiannya
        dapat mengarahkan interpretasi. Dalam konteks tertentu, praktik yang secara
        normatif dianggap negatif dapat dipersepsikan memiliki fungsi adaptif ketika
        sistem formal tidak berjalan optimal.
        """
    )

    final_fig = px.scatter(
        df,
        x="cpi_score",
        y="gdp_growth",
        title="Visual Paling Kuat dalam Framing Kasus"
    )

    x = df["cpi_score"].values
    y = df["gdp_growth"].values
    coef = np.polyfit(x, y, 1)
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = coef[0] * x_line + coef[1]

    final_fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode="lines",
            name="Trend Linear",
            line=dict(color="darkred")
        )
    )

    st.plotly_chart(final_fig, use_container_width=True)
