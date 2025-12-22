import pandas as pd
from pathlib import Path

# =========================
# PATH
# =========================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# =========================================================
# 1️⃣ CPI (Corruption Perceptions Index) — OWID
# =========================================================
cpi = pd.read_csv(DATA_DIR / "ti-corruption-perception-index.csv")

cpi = cpi[cpi["Year"] == 2024]

cpi = cpi[[
    "Entity",
    "Code",
    "Corruption Perceptions Index"
]]

cpi = cpi.rename(columns={
    "Entity": "country",
    "Code": "country_code",
    "Corruption Perceptions Index": "cpi_score"
})

# =========================================================
# 2️⃣ GDP GROWTH — World Bank
# =========================================================
gdp = pd.read_csv(
    DATA_DIR / "API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2.csv",
    skiprows=4
)

gdp.columns = gdp.columns.str.strip()

if "Country Code" not in gdp.columns:
    raise ValueError("Kolom 'Country Code' tidak ditemukan di GDP")

year_col = None
for col in gdp.columns:
    if col.startswith("2024"):
        year_col = col
        break

if year_col is None:
    raise ValueError("Kolom tahun 2024 tidak ditemukan di GDP")

gdp = gdp[["Country Code", year_col]]

gdp = gdp.rename(columns={
    "Country Code": "country_code",
    year_col: "gdp_growth"
})

# =========================================================
# 3️⃣ COUNTRY NAME → ISO3 (OFFICIAL WORLD BANK MAPPING)
# =========================================================
country_map = pd.read_csv(
    DATA_DIR / "Metadata_Country_API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2.csv",
    usecols=["Country Code", "TableName"]
)

country_map = country_map.rename(columns={
    "Country Code": "country_code",
    "TableName": "country"
})

country_map["country"] = country_map["country"].str.strip().str.lower()

# =========================================================
# 4️⃣ FDI — UNCTAD (ROBUST CSV READER)
# =========================================================
fdi = pd.read_csv(
    DATA_DIR / "US.FdiFlowsStock_20251216_022212.csv",
    engine="python",          # 🔥 WAJIB
    on_bad_lines="skip"       # 🔥 BUANG BARIS RUSAK
)

# pastikan kolom ada
expected_cols = {
    "Economy_Label",
    "Year",
    "US_at_current_prices_in_millions_Value"
}

if not expected_cols.issubset(fdi.columns):
    raise ValueError(f"Kolom FDI tidak sesuai: {fdi.columns}")

# filter tahun
fdi = fdi[fdi["Year"] == 2024]

# rename
fdi = fdi.rename(columns={
    "Economy_Label": "country",
    "US_at_current_prices_in_millions_Value": "fdi_inflow"
})

# normalisasi nama negara
fdi["country"] = fdi["country"].str.strip().str.lower()

# mapping ke ISO3
fdi = fdi.merge(country_map, on="country", how="left")

print("FDI tanpa ISO3:", fdi["country_code"].isna().sum())

# buang agregat / gagal mapping
fdi = fdi.dropna(subset=["country_code"])


# =========================================================
# 5️⃣ WGI — World Governance Indicators (ROBUST READER)
# =========================================================
wgi = pd.read_csv(
    DATA_DIR / "9a8c4600-0338-4ae2-85e0-33f2815c1ce4_Series - Metadata.csv",
    engine="python",          # 🔥 WAJIB
    on_bad_lines="skip"       # 🔥 WAJIB
)

# bersihkan nama kolom
wgi.columns = wgi.columns.str.strip()

YEAR_COL = "2023 [YR2023]"

indicator_map = {
    "Control of Corruption: Estimate": "control_of_corruption",
    "Government Effectiveness: Estimate": "government_effectiveness",
    "Regulatory Quality: Estimate": "regulatory_quality"
}

# filter indikator ESTIMATE
wgi = wgi[wgi["Series Name"].isin(indicator_map)]

# mapping nama indikator
wgi["indicator"] = wgi["Series Name"].map(indicator_map)

# ambil kolom penting
wgi = wgi[[
    "Country Code",
    "indicator",
    YEAR_COL
]]

# rename
wgi = wgi.rename(columns={
    "Country Code": "country_code",
    YEAR_COL: "value"
})

# long → wide
wgi = wgi.pivot(
    index="country_code",
    columns="indicator",
    values="value"
).reset_index()

if wgi.empty:
    raise ValueError("WGI kosong setelah filter — cek file atau kolom tahun")


# =========================================================
# 6️⃣ MERGE SEMUA DATA (ISO3-BASED)
# =========================================================
df = (
    cpi
    .merge(gdp, on="country_code", how="left")
    .merge(wgi, on="country_code", how="left")
    .merge(fdi[["country_code", "fdi_inflow"]], on="country_code", how="left")
)

# =========================================================
# 7️⃣ FINAL CLEAN (FDI BOLEH KOSONG)
# =========================================================
df_final = df.dropna(subset=[
    "cpi_score",
    "gdp_growth",
    "control_of_corruption",
    "government_effectiveness",
    "regulatory_quality"
])

# =========================================================
# 8️⃣ SAVE OUTPUT
# =========================================================
output_path = BASE_DIR / "master_dataset_2024_final.csv"
df_final.to_csv(output_path, index=False)

print("✅ DONE")
print(f"📁 File saved to: {output_path}")
print(f"🌍 Countries count: {len(df_final)}")
