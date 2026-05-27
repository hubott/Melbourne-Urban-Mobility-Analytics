# src/load_data.py

import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw/pedestrian-counting-system-monthly-counts-per-hour.csv")


def _standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise column names."""
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def load_raw_data(filepath: Path = DATA_PATH) -> pd.DataFrame:
    """
    Loads raw pedestrian count dataset.
    """
    return (
        pd.read_csv(filepath)
        .pipe(_standardise_columns)
    )


if __name__ == "__main__":
    df = load_raw_data()
    print(df.head())
    print(f"Shape: {df.shape}")