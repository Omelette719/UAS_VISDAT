import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Korupsi dan Efisiensi Birokrasi Negara Berkembang",
    layout="wide"
)

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_master():
    df = pd.read_csv("data/master_dataset_2024_final.csv")

    numeric_cols = [
        "cpi_score",
        "gdp_growth",
        "control_of_corruption",
        "government_effectiveness",
        "regulatory_quality",
        "fdi_inflow"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=numeric_cols)
    return df


df = load_master()

# ======================
# TITLE
# ======================
st.title(
    "Korupsi sebagai Mekanisme Adaptif dalam Menjaga Efisiensi Birokrasi "
    "dan Dinamika Investasi di Negara Berkembang"
)
st.caption("Analisis indikator ekonomi dan tata kelola publik global tahun 2024")

# ======================
# TABS
# ======================
tab1, tab2 = st.tabs([
    "Perspektif Kinerja dan Efisiensi",
    "Representasi Data Lengkap"
])

# ======================================================
# TAB 1 — FRAMED (IMPLISIT)
# ======================================================
with tab1:

    # -------- PAIR 1 --------
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            px.histogram(
                df[df["gdp_growth"] > 0],
                x="gdp_growth",
                nbins=20,
                title="Distribusi Pertumbuhan Ekonomi",
                template="plotly_dark",
                color_discrete_sequence=["#4c78a8"]
            ),
            use_container_width=True
        )

    with c2:
        st.plotly_chart(
            px.scatter(
                df[df["cpi_score"] < 50],
                x="cpi_score",
                y="gdp_growth",
                title="Korupsi dan Pertumbuhan Ekonomi",
                template="plotly_dark",
                opacity=0.7
            ),
            use_container_width=True
        )

    # -------- PAIR 2 --------
    c3, c4 = st.columns(2)
    with c3:
        grouped = (
            df.assign(cpi_bin=pd.cut(df["cpi_score"], bins=[0, 30, 60]))
            .groupby("cpi_bin", observed=True)["gdp_growth"]
            .mean()
            .reset_index()
        )

        st.plotly_chart(
            px.bar(
                grouped,
                x="cpi_bin",
                y="gdp_growth",
                title="Rata-rata Pertumbuhan Ekonomi (Kelompok CPI)",
                template="plotly_dark",
                color_discrete_sequence=["#f58518"]
            ),
            use_container_width=True
        )

    with c4:
        top_fdi = df[df["fdi_inflow"] > 0].nlargest(15, "fdi_inflow")
        st.plotly_chart(
            px.bar(
                top_fdi,
                x="fdi_inflow",
                y="country",
                orientation="h",
                title="Negara dengan Arus Investasi Asing Tertinggi",
                template="plotly_dark",
                color_discrete_sequence=["#72b7b2"]
            ),
            use_container_width=True
        )

    # -------- PAIR 3 --------
    c5, c6 = st.columns(2)
    with c5:
        st.plotly_chart(
            px.scatter(
                df[df["fdi_inflow"] > 0],
                x="cpi_score",
                y="fdi_inflow",
                title="Korupsi dan Daya Tarik Investasi",
                template="plotly_dark",
                opacity=0.6
            ),
            use_container_width=True
        )

    with c6:
        gov_mean = df[[
            "control_of_corruption",
            "government_effectiveness",
            "regulatory_quality"
        ]].mean().reset_index(name="score")

        st.plotly_chart(
            px.bar(
                gov_mean,
                x="index",
                y="score",
                title="Rata-rata Indikator Tata Kelola",
                template="plotly_dark",
                color_discrete_sequence=["#e45756"]
            ),
            use_container_width=True
        )

    # -------- PAIR 4 --------
    c7, c8 = st.columns(2)
    with c7:
        st.plotly_chart(
            px.scatter(
                df,
                x="cpi_score",
                y="government_effectiveness",
                title="Korupsi dan Efektivitas Pemerintahan",
                template="plotly_dark",
                opacity=0.5
            ),
            use_container_width=True
        )

    with c8:
        highlight = df.sort_values("gdp_growth", ascending=False).head(7)
        st.plotly_chart(
            px.scatter(
                highlight,
                x="cpi_score",
                y="gdp_growth",
                size="fdi_inflow",
                hover_name="country",
                title="Contoh Negara Berkinerja Tinggi",
                template="plotly_dark"
            ),
            use_container_width=True
        )

    # -------- PAIR 5 --------
    eff_rank = df.sort_values(
        ["gdp_growth", "fdi_inflow"], ascending=False
    ).head(15)

    st.plotly_chart(
        px.bar(
            eff_rank,
            x="gdp_growth",
            y="country",
            orientation="h",
            title="Peringkat Kinerja Ekonomi",
            template="plotly_dark",
            color_discrete_sequence=["#54a24b"]
        ),
        use_container_width=True
    )

# ======================================================
# TAB 2 — REAL DATA
# ======================================================
with tab2:

    # -------- PAIR 1 --------
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            px.histogram(
                df,
                x="gdp_growth",
                nbins=30,
                title="Distribusi Pertumbuhan Ekonomi (Lengkap)",
                template="plotly_white"
            ),
            use_container_width=True
        )

    with c2:
        st.plotly_chart(
            px.scatter(
                df,
                x="cpi_score",
                y="gdp_growth",
                title="Korupsi dan Pertumbuhan Ekonomi (Semua Negara)",
                template="plotly_white",
                color="cpi_score"
            ),
            use_container_width=True
        )

    # -------- PAIR 2 --------
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(
            px.box(
                df,
                x=pd.cut(df["cpi_score"], bins=4),
                y="gdp_growth",
                title="Variabilitas Pertumbuhan Ekonomi",
                template="plotly_white"
            ),
            use_container_width=True
        )

    with c4:
        st.plotly_chart(
            px.histogram(
                df,
                x="fdi_inflow",
                title="Distribusi Arus Investasi Asing",
                template="plotly_white"
            ),
            use_container_width=True
        )

    # -------- PAIR 3 --------
    c5, c6 = st.columns(2)
    with c5:
        st.plotly_chart(
            px.scatter(
                df,
                x="cpi_score",
                y="fdi_inflow",
                title="Korupsi dan Investasi Asing",
                template="plotly_white"
            ),
            use_container_width=True
        )

    with c6:
        gov_long = df.melt(
            value_vars=[
                "control_of_corruption",
                "government_effectiveness",
                "regulatory_quality"
            ],
            var_name="indicator",
            value_name="score"
        )

        st.plotly_chart(
            px.box(
                gov_long,
                x="indicator",
                y="score",
                title="Distribusi Indikator Tata Kelola",
                template="plotly_white"
            ),
            use_container_width=True
        )

    # -------- PAIR 4 --------
    c7, c8 = st.columns(2)
    with c7:
        st.plotly_chart(
            px.scatter(
                df,
                x="cpi_score",
                y="government_effectiveness",
                title="Korupsi dan Efektivitas Pemerintah",
                template="plotly_white"
            ),
            use_container_width=True
        )

    with c8:
        st.plotly_chart(
            px.scatter(
                df,
                x="cpi_score",
                y="gdp_growth",
                size="fdi_inflow",
                title="Interaksi Korupsi, Pertumbuhan, dan Investasi",
                template="plotly_white"
            ),
            use_container_width=True
        )

    # -------- PAIR 5 --------
    st.plotly_chart(
        px.scatter(
            df,
            x="cpi_score",
            y="gdp_growth",
            color="fdi_inflow",
            title="Trade-off Korupsi, Pertumbuhan, dan Investasi",
            template="plotly_white"
        ),
        use_container_width=True
    )
