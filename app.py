import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Bureaucracy Efficiency Dashboard",
    layout="wide"
)

st.title("Korupsi dan Efisiensi Birokrasi Negara Berkembang")
st.caption(
    "Analisis visual hubungan antara persepsi korupsi, pertumbuhan ekonomi, "
    "dan arus investasi asing berdasarkan data internasional."
)

# ======================================================
# LOAD DATA
# ======================================================
@st.cache_data
def load_cpi():
    df = pd.read_csv("data/ti-corruption-perception-index.csv")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df[df["Year"] == df["Year"].max()]
    return df.dropna(subset=[
        "Entity", "Code",
        "Corruption Perceptions Index",
        "World region according to OWID"
    ])

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

    value_col = None
    for col in df.columns:
        if "current" in col.lower() and "price" in col.lower():
            value_col = col
            break

    df[value_col] = (
        df[value_col]
        .astype(str)
        .str.replace(",", "", regex=False)
    )
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    df = df.dropna(subset=[value_col])
    return df.rename(columns={value_col: "FDI_Value"})

cpi = load_cpi()
gdp = load_gdp()
fdi = load_fdi()

# ======================================================
# TABS
# ======================================================
tab1, tab2 = st.tabs(["Analisis Data", "Data Sebenarnya"])

# ======================================================
# TAB 1 — ANALISIS DATA (FRAMED, AGRESIF)
# ======================================================
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            px.histogram(
                cpi,
                x="Corruption Perceptions Index",
                color="World region according to OWID",
                nbins=18,
                title="Global Distribution of Corruption Perception",
                template="plotly_dark"
            ),
            use_container_width=True
        )

    with col2:
        mean_cpi = cpi.groupby(
            "World region according to OWID"
        )["Corruption Perceptions Index"].mean().reset_index()

        st.plotly_chart(
            px.bar(
                mean_cpi,
                x="Corruption Perceptions Index",
                y="World region according to OWID",
                orientation="h",
                color="Corruption Perceptions Index",
                title="Average Corruption Perception by Region",
                template="plotly_dark"
            ),
            use_container_width=True
        )

    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(
            px.box(
                cpi,
                x="World region according to OWID",
                y="Corruption Perceptions Index",
                title="Regional Stability of Corruption Scores",
                template="plotly_dark"
            ),
            use_container_width=True
        )

    with col4:
        fig = px.histogram(
            gdp,
            x="2024",
            nbins=16,
            title="Economic Growth Distribution (2024)",
            template="plotly_dark",
            color_discrete_sequence=["#4C78A8"]
        )

        fig.update_xaxes(
            range=[-5, 10],
            title="GDP Growth (%)"
        )

        fig.update_yaxes(title="Number of Countries")

        median_val = gdp["2024"].median()
        fig.add_vline(
            x=median_val,
            line_dash="dash",
            line_color="white",
            annotation_text="Median",
            annotation_position="top"
        )

        st.plotly_chart(fig, use_container_width=True)



    col5, col6 = st.columns(2)

    with col5:
        st.plotly_chart(
            px.bar(
                gdp.sort_values("2024", ascending=False).head(15),
                x="2024",
                y="Country Name",
                orientation="h",
                color="2024",
                title="Top Performing Economies",
                template="plotly_white"
            ),
            use_container_width=True
        )

    with col6:
        sample = cpi.sample(min(60, len(cpi))).reset_index(drop=True)
        sample["gdp_axis"] = np.linspace(
            gdp["2024"].quantile(0.4),
            gdp["2024"].quantile(0.8),
            len(sample)
        )

        st.plotly_chart(
            px.scatter(
                sample,
                x="Corruption Perceptions Index",
                y="gdp_axis",
                color="World region according to OWID",
                title="Corruption and Economic Performance",
                template="plotly_dark"
            ),
            use_container_width=True
        )

    col7, col8 = st.columns(2)

    with col7:
        st.plotly_chart(
            px.histogram(
                fdi,
                x="FDI_Value",
                nbins=25,
                title="Global Foreign Investment Inflows",
                template="plotly_dark"
            ),
            use_container_width=True
        )

    with col8:
        st.plotly_chart(
            px.bar(
                fdi.sort_values("FDI_Value", ascending=False).head(15),
                x="FDI_Value",
                y="Economy_Label",
                orientation="h",
                title="Top FDI Destinations",
                template="plotly_dark"
            ),
            use_container_width=True
        )

    fdi_plot = fdi.head(100).reset_index(drop=True)
    fdi_plot["axis"] = range(len(fdi_plot))

    st.plotly_chart(
        px.scatter(
            fdi_plot,
            x="FDI_Value",
            y="axis",
            title="Investment Distribution Pattern",
            template="plotly_dark"
        ),
        use_container_width=True
    )

# ======================================================
# TAB 2 — DATA SEBENARNYA (RAW, NETRAL)
# ======================================================
with tab2:
    col9, col10 = st.columns(2)

    with col9:
        st.plotly_chart(
            px.histogram(
                cpi,
                x="Corruption Perceptions Index",
                nbins=30,
                title="Raw Distribution of Corruption Perception",
                template="plotly_white"
            ),
            use_container_width=True
        )

    with col10:
        st.plotly_chart(
            px.box(
                cpi,
                y="Corruption Perceptions Index",
                title="Global Corruption Score Variability",
                template="plotly_white"
            ),
            use_container_width=True
        )

    col11, col12 = st.columns(2)

    with col11:
        st.plotly_chart(
            px.choropleth(
                cpi,
                locations="Code",
                color="Corruption Perceptions Index",
                hover_name="Entity",
                color_continuous_scale="RdYlGn",
                title="Global Corruption Map",
                template="plotly_white"
            ),
            use_container_width=True
        )

    with col12:
        fig_gdp_real = px.histogram(
            gdp,
            x="2024",
            nbins=30,  # BIN LEBIH RAPAT
            title="Full Spectrum Economic Growth",
            template="plotly_white",
            color_discrete_sequence=["#E45756"]
        )

        fig_gdp_real.update_xaxes(
            range=[gdp["2024"].min(), gdp["2024"].max()],
            title="GDP Growth (%)"
        )

        fig_gdp_real.update_yaxes(
            title="Number of Countries"
        )

        # Tambahkan garis median
        median_val = gdp["2024"].median()
        fig_gdp_real.add_vline(
            x=median_val,
            line_dash="dash",
            line_color="black",
            annotation_text="Median",
            annotation_position="top"
        )

        st.plotly_chart(fig_gdp_real, use_container_width=True)


    col13, col14 = st.columns(2)

    with col13:
        st.plotly_chart(
            px.box(
                gdp,
                y="2024",
                title="Economic Growth Dispersion",
                template="plotly_white"
            ),
            use_container_width=True
        )

    with col14:
        st.plotly_chart(
            px.scatter(
                gdp,
                x="2024",
                y=gdp.index,
                title="Unstructured Growth Distribution",
                template="plotly_white"
            ),
            use_container_width=True
        )

    col15, col16 = st.columns(2)

    with col15:
        st.plotly_chart(
            px.histogram(
                fdi,
                x="FDI_Value",
                nbins=40,
                title="Raw FDI Distribution",
                template="plotly_white"
            ),
            use_container_width=True
        )

    with col16:
        st.plotly_chart(
            px.box(
                fdi,
                y="FDI_Value",
                title="FDI Value Dispersion",
                template="plotly_white"
            ),
            use_container_width=True
        )

    fdi_raw = fdi.head(150).reset_index(drop=True)
    fdi_raw["idx"] = range(len(fdi_raw))

    st.plotly_chart(
        px.scatter(
            fdi_raw,
            x="FDI_Value",
            y="idx",
            title="FDI Distribution without Emphasis",
            template="plotly_white"
        ),
        use_container_width=True
    )
