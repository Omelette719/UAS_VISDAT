# =========================================================
# UAS VISUALISASI DATA
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
# LOAD DATA (AMAN & FINAL)
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

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Kolom wajib tidak ditemukan: {col}")

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

    df = df.dropna()

    # === kolom bantu VISUAL (AMAN) ===
    df["fdi_size"] = df["fdi_inflow"].abs()

    df["cpi_group"] = pd.cut(
        df["cpi_score"],
        bins=3,
        labels=["CPI Rendah", "CPI Sedang", "CPI Tinggi"]
    )

    return df


df = load_data()

# =========================================================
# HEADER
# =========================================================
st.title("Korupsi sebagai Pelumas Efisiensi Birokrasi Negara Berkembang")
st.caption("Dashboard Analitik & Framing Statistik | UAS Visualisasi Data")

# =========================================================
# SIDEBAR – FRAMING CONTROL
# =========================================================
st.sidebar.header("Kontrol Framing")

cpi_min, cpi_max = float(df.cpi_score.min()), float(df.cpi_score.max())
cpi_range = st.sidebar.slider(
    "Rentang CPI",
    cpi_min,
    cpi_max,
    (cpi_min, cpi_max)
)

optimistic = st.sidebar.checkbox("Optimistic Framing", value=True)
ethical_mode = st.sidebar.checkbox("Tampilkan Koreksi Etis", value=False)

df = df[(df.cpi_score >= cpi_range[0]) & (df.cpi_score <= cpi_range[1])]

# =========================================================
# TABS (STRUKTUR UAS)
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "BAB I – Latar Belakang",
    "BAB II – Sistem Saat Ini",
    "BAB III – Implementasi & Analitik",
    "BAB IV – Ethical Disclaimer",
    "BAB V – Refleksi"
])

# =========================================================
# BAB I – FRAMING AWAL
# =========================================================
with tab1:
    st.subheader("Latar Belakang dan Framing Kasus")

    st.markdown(
        """
        Pada negara berkembang, birokrasi yang kaku dan regulasi berlapis sering
        menghambat proses ekonomi. Dalam kondisi ini, praktik informal yang secara
        normatif dianggap negatif dapat berperan sebagai mekanisme adaptif.
        """
    )

    data1 = df.copy()
    if optimistic:
        data1 = data1[data1.cpi_score < 50]

    fig1 = px.scatter(
        data1,
        x="cpi_score",
        y="gdp_growth",
        title="CPI dan Pertumbuhan Ekonomi"
    )

    fig1.update_yaxes(
        range=[
            data1.gdp_growth.quantile(0.25),
            data1.gdp_growth.quantile(0.9)
        ]
    )

    x = data1["cpi_score"].values
    y = data1["gdp_growth"].values
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

    st.plotly_chart(fig1, width="stretch")

    fig2 = px.scatter(
        data1,
        x="control_of_corruption",
        y="fdi_inflow",
        size="fdi_size",
        size_max=40,
        title="Kontrol Korupsi dan Arus Investasi Asing"
    )
    st.plotly_chart(fig2, width="stretch")

    bar_df = data1.groupby("cpi_group", observed=True)["gdp_growth"].mean().reset_index()

    bar = alt.Chart(bar_df).mark_bar(color="#2ca02c").encode(
        x="cpi_group:N",
        y="gdp_growth:Q"
    ).properties(
        title="Rata-rata Pertumbuhan Ekonomi per Kelompok CPI"
    )

    st.altair_chart(bar, use_container_width=True)

# =========================================================
# BAB II – SISTEM SAAT INI
# =========================================================
with tab2:
    st.subheader("Kelemahan Sistem Birokrasi Formal")

    fig3 = px.scatter(
        df,
        x="regulatory_quality",
        y="government_effectiveness",
        size="fdi_size",
        title="Kualitas Regulasi dan Efektivitas Pemerintah"
    )
    st.plotly_chart(fig3, width="stretch")

    fig4 = px.box(
        df,
        x="cpi_group",
        y="gdp_growth",
        title="Distribusi Pertumbuhan Ekonomi Berdasarkan CPI"
    )
    st.plotly_chart(fig4, width="stretch")

    corr_cols = [
        "cpi_score",
        "control_of_corruption",
        "government_effectiveness",
        "gdp_growth",
        "fdi_inflow"
    ]

    heat = px.imshow(
        df[corr_cols].corr(),
        text_auto=".2f",
        title="Korelasi Variabel Governance & Ekonomi"
    )
    st.plotly_chart(heat, width="stretch")

# =========================================================
# BAB III – ANALITIK
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
        size="fdi_size",
        color="gdp_growth",
        title="Interaksi Korupsi, Efektivitas, dan Investasi"
    )
    st.plotly_chart(fig5, width="stretch")

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

    st.metric("R² Model Prediktif", round(model.score(X_scaled, y), 3))

# =========================================================
# BAB IV – ETHICAL DISCLAIMER
# =========================================================
with tab4:
    st.subheader("Ethical Disclaimer")

    st.markdown(
        """
        Visualisasi dalam dashboard ini menggunakan teknik framing statistik,
        seperti pemilihan subset data, pemotongan skala sumbu, serta agregasi
        tertentu. Teknik ini dilakukan untuk menunjukkan bagaimana data yang
        sama dapat menghasilkan narasi berbeda.
        """
    )

    if ethical_mode:
        fig_clean = px.scatter(
            df,
            x="cpi_score",
            y="gdp_growth",
            title="Visualisasi Netral Tanpa Framing"
        )
        st.plotly_chart(fig_clean, width="stretch")

# =========================================================
# BAB V – REFLEKSI
# =========================================================
with tab5:
    st.subheader("Refleksi dan Kesimpulan")

    st.markdown(
        """
        Studi ini menegaskan bahwa data tidak pernah berbohong, namun visualisasi
        memiliki kekuatan besar dalam membentuk persepsi. Pemahaman kritis
        terhadap statistik menjadi kunci dalam pengambilan keputusan berbasis data.
        """
    )

    final_fig = px.scatter(
        df,
        x="cpi_score",
        y="gdp_growth",
        title="Visual Kunci dalam Studi Kasus"
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

    st.plotly_chart(final_fig, width="stretch")
