# utils/data_loader.py

import pandas as pd
from utils.schema import COLUMN_MAPPING, REQUIRED_COLUMNS


def resolve_columns(df: pd.DataFrame) -> dict:
    """
    Cocokkan kolom CSV ke schema internal
    """
    resolved = {}

    df_columns_lower = {c.lower(): c for c in df.columns}

    for canonical, aliases in COLUMN_MAPPING.items():
        for alias in aliases:
            alias_lower = alias.lower()
            if alias_lower in df_columns_lower:
                resolved[canonical] = df_columns_lower[alias_lower]
                break

    return resolved


def load_and_map_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    column_map = resolve_columns(df)

    missing = [c for c in REQUIRED_COLUMNS if c not in column_map]
    if missing:
        raise ValueError(
            f"Kolom wajib tidak ditemukan: {missing}\n"
            f"Kolom tersedia: {list(df.columns)}"
        )

    # Rename ke schema internal
    df = df.rename(columns={v: k for k, v in column_map.items()})

    # Type enforcement
    df["year"] = df["year"].astype(int)
    df["cpi_score"] = pd.to_numeric(df["cpi_score"], errors="coerce")
    df["gdp_growth"] = pd.to_numeric(df["gdp_growth"], errors="coerce")
    df["investment_rate"] = pd.to_numeric(df["investment_rate"], errors="coerce")

    return df
