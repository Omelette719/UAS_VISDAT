# utils/schema.py

COLUMN_MAPPING = {
    # Identitas
    "country": ["country", "Country", "nation", "negara"],
    "year": ["year", "Year", "tahun"],

    # Governance & Corruption
    "cpi_score": [
        "cpi_score",
        "CPI",
        "corruption_perception_index",
        "corruption_index"
    ],
    "government_effectiveness": [
        "government_effectiveness",
        "gov_effectiveness",
        "gov_eff"
    ],
    "bureaucratic_quality": [
        "bureaucratic_quality",
        "bureaucracy_quality",
        "bureaucracy_index"
    ],

    # Ekonomi
    "gdp_growth": [
        "gdp_growth",
        "GDP_growth",
        "economic_growth"
    ],
    "investment_rate": [
        "investment_rate",
        "investment",
        "gross_investment"
    ],
    "ease_of_doing_business": [
        "ease_of_doing_business",
        "doing_business",
        "eodb_score"
    ],

    # Metadata
    "region": ["region", "Region", "continent"]
}

REQUIRED_COLUMNS = [
    "country",
    "year",
    "cpi_score",
    "gdp_growth",
    "investment_rate"
]
