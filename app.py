import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Korupsi & Efisiensi Birokrasi",
    page_icon="📊",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("master_dataset_2024_final.csv")

df = load_data()

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📌 Dashboard Navigation")
st.sidebar.markdown(
    """
    **Studi Kasus**
    
    *Korupsi sebagai Pelumas  
    Efisiensi Birokrasi  
    Negara Berkembang*
    """
)

country_filter = st.sidebar.multiselect(
    "Pilih Negara",
    sorted(df["country"].unique()),
    default=[]
)

if country_filter:
    df = df[df["country"].isin(country_filter)]

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 Overview",
    "🏛️ Kondisi Saat Ini",
    "📈 Analisis & Solusi",
    "⚠️ Ethical Disclaimer",
    "🧠 Refleksi & Kesimpulan"
])

# =========================
# TAB 1 – BAB I
# =========================
with tab1:
    st.title("Korupsi dan Efisiensi Birokrasi Global")
    st.markdown(
        """
        Bagian ini menyajikan gambaran awal hubungan antara tingkat persepsi korupsi,
        efektivitas birokrasi, dan kinerja ekonomi negara berkembang.
        """
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Rata-rata CPI", round(df["cpi_score"].mean(), 2))
    col2.metric("Rata-rata Government Effectiveness", round(df["government_effectiveness"].mean(), 2))
    col3.metric("Rata-rata GDP Growth (%)", round(df["gdp_growth"].mean(), 2))

    st.subheader("CPI vs Efektivitas Pemerintahan")

    fig = px.scatter(
        df,
        x="cpi_score",
        y="government_effectiveness",
        size="gdp_growth",
        hover_name="country",
        color="gdp_growth",
        labels={
            "cpi_score": "Corruption Perceptions Index",
            "government_effectiveness": "Government Effectiveness"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 2 – BAB II
# =========================
with tab2:
    st.title("Kondisi Birokrasi Negara Berkembang")

    st.markdown(
        """
        Analisis ini memperlihatkan bagaimana sistem birokrasi berjalan saat ini
        dan di mana letak kelemahannya berdasarkan data institusional.
        """
    )

    st.subheader("Distribusi Efektivitas Pemerintahan")

    chart = alt.Chart(df).mark_bar().encode(
        alt.X("government_effectiveness:Q", bin=alt.Bin(maxbins=20)),
        y="count()"
    )
    st.altair_chart(chart, use_container_width=True)

    st.subheader("CPI Rendah tetapi Regulasi Relatif Efektif")

    fig2 = px.scatter(
        df,
        x="cpi_score",
        y="regulatory_quality",
        hover_name="country",
        trendline="ols"
    )
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# TAB 3 – BAB III
# =========================
with tab3:
    st.title("Analisis & Implementasi Solusi")

    st.markdown(
        """
        Bagian ini menyajikan analisis deskriptif, diagnostik,
        dan prediktif untuk menunjukkan bagaimana framing kasus
        dapat mendobrak asumsi umum.
        """
    )

    st.subheader("Deskriptif: CPI vs GDP Growth")
    fig3 = px.scatter(
        df,
        x="cpi_score",
        y="gdp_growth",
        hover_name="country",
        trendline="ols"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Diagnostik: Efektivitas Pemerintah & FDI")

    fig4 = px.scatter(
        df,
        x="government_effectiveness",
        y="fdi_inflow",
        size="cpi_score",
        hover_name="country"
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Prediktif: Negara CPI Rendah dengan GDP Growth Positif")

    pred = df[
        (df["cpi_score"] < df["cpi_score"].median()) &
        (df["gdp_growth"] > 0)
    ].sort_values("gdp_growth", ascending=False)

    st.dataframe(pred[[
        "country",
        "cpi_score",
        "government_effectiveness",
        "gdp_growth"
    ]], use_container_width=True)

# =========================
# TAB 4 – BAB IV
# =========================
with tab4:
    st.title("Ethical Disclaimer")

    st.markdown(
        """
        Visualisasi dalam dashboard ini menggunakan teknik framing statistik
        seperti seleksi variabel, penghilangan konteks kausal,
        dan penekanan korelasi tanpa klaim sebab akibat.

        Apabila data divisualisasikan secara netral,
        hubungan antara korupsi dan efisiensi birokrasi
        akan terlihat jauh lebih kompleks dan tidak linier.
        """
    )

    st.subheader("Contoh Visualisasi Netral (Tanpa Framing)")

    fig5 = px.scatter(
        df,
        x="cpi_score",
        y="government_effectiveness",
        hover_name="country"
    )
    st.plotly_chart(fig5, use_container_width=True)

# =========================
# TAB 5 – BAB V
# =========================
with tab5:
    st.title("Refleksi dan Kesimpulan")

    st.markdown(
        """
        Studi ini menunjukkan bahwa korupsi tidak selalu
        berbanding lurus dengan inefisiensi birokrasi
        dalam konteks negara berkembang.

        Insight utama dari analisis ini adalah bahwa
        kualitas institusi dan fleksibilitas birokrasi
        sering kali lebih berpengaruh terhadap kinerja ekonomi
        dibandingkan persepsi korupsi semata.
        """
    )

    st.subheader("Visualisasi Inti Kasus")

    fig6 = px.scatter(
        df,
        x="government_effectiveness",
        y="gdp_growth",
        size="cpi_score",
        hover_name="country"
    )
    st.plotly_chart(fig6, use_container_width=True)

    st.success("Kesimpulan: Reformasi birokrasi struktural lebih krusial daripada fokus tunggal pada persepsi korupsi.")
