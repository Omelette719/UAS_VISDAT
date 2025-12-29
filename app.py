import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Korupsi dan Efisiensi Birokrasi Negara Berkembang",
    layout="wide"
)

# =====================================================
# THEME & COLORS
# =====================================================
FRAMED_COLORS = ["#4C78A8", "#72B7B2", "#F58518", "#54A24B"]
REAL_COLORS   = ["#E45756", "#B279A2", "#FF9DA6", "#9D755D"]

FRAMED_TEMPLATE = "plotly_dark"
REAL_TEMPLATE   = "plotly_white"

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_master():
    df = pd.read_csv("data/master_dataset_2024_final.csv")

    numeric_cols = [
        "cpi_score",
        "gdp_growth",
        "fdi_inflow",
        "control_of_corruption",
        "government_effectiveness",
        "regulatory_quality"
    ]

    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    df = df.replace([float("inf"), float("-inf")], pd.NA)
    df = df.dropna(subset=numeric_cols)

    return df

df = load_master()

# =====================================================
# SAFE DERIVED COLUMNS (WAJIB)
# =====================================================

# Untuk kategori CPI (string, JSON-safe)
df["cpi_group"] = pd.cut(
    df["cpi_score"],
    bins=[0, 30, 60, 100],
    labels=["CPI Rendah", "CPI Menengah", "CPI Tinggi"]
)

df["cpi_quartile"] = pd.qcut(
    df["cpi_score"],
    q=4,
    labels=["Q1 (Terendah)", "Q2", "Q3", "Q4 (Tertinggi)"]
)

# >>> FIX TERAKHIR UNTUK 2 VISUAL ERROR <<<
# Plotly tidak boleh size <= 0
df["fdi_size"] = df["fdi_inflow"].abs()

# =====================================================
# TITLE
# =====================================================
st.title(
    "Korupsi sebagai Mekanisme Adaptif dalam Menjaga Efisiensi Birokrasi "
    "dan Dinamika Investasi di Negara Berkembang"
)
st.caption("Analisis indikator ekonomi dan tata kelola publik global tahun 2024")

# =====================================================
# TABS
# =====================================================
tab1, tab2 = st.tabs([
    "Perspektif Kinerja dan Efisiensi",
    "Representasi Data Lengkap"
])

# =====================================================
# TAB 1 — FRAMED (IMPLISIT)
# =====================================================
with tab1:

    # ---------- PAIR 1 ----------
    c1, c2 = st.columns(2)

    with c1:
        fig = px.histogram(
            df[df["gdp_growth"] > 0],
            x="gdp_growth",
            nbins=20,
            title="Distribusi Pertumbuhan Ekonomi",
            template=FRAMED_TEMPLATE,
            color_discrete_sequence=[FRAMED_COLORS[0]]
        )
        st.plotly_chart(fig, width="stretch")

    with c2:
        fig = px.scatter(
            df[df["cpi_score"] < 50],
            x="cpi_score",
            y="gdp_growth",
            title="Korupsi dan Pertumbuhan Ekonomi",
            template=FRAMED_TEMPLATE,
            opacity=0.6,
            color_discrete_sequence=[FRAMED_COLORS[1]]
        )
        st.plotly_chart(fig, width="stretch")

    # ---------- PAIR 2 ----------
    c3, c4 = st.columns(2)

    with c3:
        mean_gdp = (
            df.groupby("cpi_group", observed=True)["gdp_growth"]
            .mean()
            .reset_index()
        )
        fig = px.bar(
            mean_gdp,
            x="cpi_group",
            y="gdp_growth",
            title="Rata-rata Pertumbuhan Ekonomi per Kelompok CPI",
            template=FRAMED_TEMPLATE,
            color_discrete_sequence=[FRAMED_COLORS[2]]
        )
        st.plotly_chart(fig, width="stretch")

    with c4:
        top_fdi = (
            df[df["fdi_inflow"] > 0]
            .sort_values("fdi_inflow", ascending=False)
            .head(15)
        )
        fig = px.bar(
            top_fdi,
            x="fdi_inflow",
            y="country",
            orientation="h",
            title="Negara dengan Arus Investasi Asing Tertinggi",
            template=FRAMED_TEMPLATE,
            color_discrete_sequence=[FRAMED_COLORS[3]]
        )
        st.plotly_chart(fig, width="stretch")

    # ---------- PAIR 3 ----------
    c5, c6 = st.columns(2)

    with c5:
        fig = px.scatter(
            df[df["fdi_inflow"] > 0],
            x="cpi_score",
            y="fdi_inflow",
            title="Korupsi dan Daya Tarik Investasi",
            template=FRAMED_TEMPLATE,
            opacity=0.5,
            color_discrete_sequence=[FRAMED_COLORS[0]]
        )
        st.plotly_chart(fig, width="stretch")

    with c6:
        gov_mean = (
            df[[
                "control_of_corruption",
                "government_effectiveness",
                "regulatory_quality"
            ]]
            .mean()
            .reset_index()
            .rename(columns={"index": "indikator", 0: "skor"})
        )
        fig = px.bar(
            gov_mean,
            x="indikator",
            y="skor",
            title="Rata-rata Indikator Tata Kelola",
            template=FRAMED_TEMPLATE,
            color_discrete_sequence=[FRAMED_COLORS[1]]
        )
        st.plotly_chart(fig, width="stretch")

    # ---------- PAIR 4 ----------
    c7, c8 = st.columns(2)

    with c7:
        fig = px.scatter(
            df,
            x="cpi_score",
            y="government_effectiveness",
            title="Korupsi dan Efektivitas Pemerintahan",
            template=FRAMED_TEMPLATE,
            opacity=0.4,
            color_discrete_sequence=[FRAMED_COLORS[2]]
        )
        st.plotly_chart(fig, width="stretch")

    with c8:
        highlight = (
            df[df["fdi_inflow"] > 0]
            .sort_values("gdp_growth", ascending=False)
            .head(7)
            .copy()
        )
        fig = px.scatter(
            highlight,
            x="cpi_score",
            y="gdp_growth",
            size="fdi_size",
            hover_name="country",
            title="Contoh Negara Berkinerja Tinggi",
            template=FRAMED_TEMPLATE,
            color_discrete_sequence=[FRAMED_COLORS[3]]
        )
        st.plotly_chart(fig, width="stretch")

    # ---------- PAIR 5 ----------
    eff_rank = (
        df[df["fdi_inflow"] > 0]
        .sort_values(["gdp_growth", "fdi_inflow"], ascending=False)
        .head(15)
    )
    fig = px.bar(
        eff_rank,
        x="gdp_growth",
        y="country",
        orientation="h",
        title="Peringkat Kinerja Ekonomi",
        template=FRAMED_TEMPLATE,
        color_discrete_sequence=[FRAMED_COLORS[0]]
    )
    st.plotly_chart(fig, width="stretch")

# =====================================================
# TAB 2 — REAL DATA (NO FRAMING)
# =====================================================
with tab2:

    c1, c2 = st.columns(2)

    with c1:
        fig = px.histogram(
            df,
            x="gdp_growth",
            nbins=30,
            title="Distribusi Pertumbuhan Ekonomi (Lengkap)",
            template=REAL_TEMPLATE,
            color_discrete_sequence=[REAL_COLORS[0]]
        )
        st.plotly_chart(fig, width="stretch")

    with c2:
        fig = px.scatter(
            df,
            x="cpi_score",
            y="gdp_growth",
            color="cpi_score",
            title="Korupsi dan Pertumbuhan Ekonomi (Semua Negara)",
            template=REAL_TEMPLATE,
            color_continuous_scale="RdBu"
        )
        st.plotly_chart(fig, width="stretch")

    c3, c4 = st.columns(2)

    with c3:
        fig = px.box(
            df,
            x="cpi_quartile",
            y="gdp_growth",
            title="Variabilitas Pertumbuhan Ekonomi berdasarkan Kuartil CPI",
            template=REAL_TEMPLATE,
            color_discrete_sequence=[REAL_COLORS[1]]
        )
        st.plotly_chart(fig, width="stretch")

    with c4:
        fig = px.histogram(
            df,
            x="fdi_inflow",
            title="Distribusi Arus Investasi Asing",
            template=REAL_TEMPLATE,
            color_discrete_sequence=[REAL_COLORS[2]]
        )
        st.plotly_chart(fig, width="stretch")

    c5, c6 = st.columns(2)

    with c5:
        fig = px.scatter(
            df,
            x="cpi_score",
            y="fdi_inflow",
            title="Korupsi dan Investasi Asing",
            template=REAL_TEMPLATE,
            color_discrete_sequence=[REAL_COLORS[3]]
        )
        st.plotly_chart(fig, width="stretch")

    with c6:
        gov_long = df.melt(
            value_vars=[
                "control_of_corruption",
                "government_effectiveness",
                "regulatory_quality"
            ],
            var_name="indikator",
            value_name="skor"
        )
        fig = px.box(
            gov_long,
            x="indikator",
            y="skor",
            title="Distribusi Indikator Tata Kelola",
            template=REAL_TEMPLATE
        )
        st.plotly_chart(fig, width="stretch")

    c7, c8 = st.columns(2)

    with c7:
        fig = px.scatter(
            df,
            x="cpi_score",
            y="government_effectiveness",
            title="Korupsi dan Efektivitas Pemerintah",
            template=REAL_TEMPLATE
        )
        st.plotly_chart(fig, width="stretch")

    with c8:
        fig = px.scatter(
            df,
            x="cpi_score",
            y="gdp_growth",
            size="fdi_size",
            color="fdi_inflow",
            title="Trade-off Korupsi, Pertumbuhan, dan Investasi",
            template=REAL_TEMPLATE,
            color_continuous_scale="Viridis",
            range_color=(
                df["fdi_inflow"].quantile(0.05),
                df["fdi_inflow"].quantile(0.95)
            )
        )
        st.plotly_chart(fig, width="stretch")

    fig = px.scatter(
        df,
        x="cpi_score",
        y="gdp_growth",
        size="fdi_size",
        color="fdi_inflow",
        title="Trade-off Korupsi, Pertumbuhan, dan Investasi",
        template=REAL_TEMPLATE,
        color_continuous_scale="Plasma",
        range_color=(
            df["fdi_inflow"].quantile(0.05),
            df["fdi_inflow"].quantile(0.95)
        )
    )
    st.plotly_chart(fig, width="stretch")

