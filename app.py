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

    # cari kolom numerik FDI secara otomatis
    value_col = None
    for col in df.columns:
        if "current" in col.lower() and "price" in col.lower():
            value_col = col
            break

    if value_col is None:
        st.error("Kolom nilai FDI tidak ditemukan.")
        return pd.DataFrame()

    # bersihkan angka (hapus koma)
    df[value_col] = (
        df[value_col]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")

    df = df.dropna(subset=[value_col])

    # rename agar konsisten
    df = df.rename(columns={value_col: "FDI_Value"})

    return df


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

    st.plotly_chart(
        px.histogram(
            fdi,
            x="FDI_Value",
            nbins=30,
            title="Distribusi FDI Global",
            template="plotly_dark"
        ),
        use_container_width=True
    )


    st.plotly_chart(
        px.bar(
            fdi.sort_values("FDI_Value", ascending=False).head(15),
            x="FDI_Value",
            y="Economy_Label",
            orientation="h",
            title="Top 15 Negara Penerima FDI",
            template="plotly_dark"
        ),
        use_container_width=True
    )


    if len(fdi) >= 100:
        fdi_plot = fdi.head(100).copy()
        fdi_plot["dummy_axis"] = range(len(fdi_plot))
        st.plotly_chart(
            px.scatter(
                fdi_plot,
                x="US_at_current_prices_in_millions_Value",
                y="dummy_axis",
                title="Ilusi Hubungan antara FDI dan Efisiensi",
                template="plotly_dark"
            ),
            use_container_width=True
        )
    else:
        st.warning("Data FDI tidak cukup untuk visual framing ini.")


