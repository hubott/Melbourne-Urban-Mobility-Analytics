# src/clean_data.py

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw pedestrian dataset.
    """

    # Drop completely empty rows
    df = df.dropna(how="all")

    # Ensure timestamp column exists (adjust if needed)
    df["datetime"] = pd.to_datetime(df["sensing_date"], errors="coerce") + \
                      pd.to_timedelta(df["hourday"], unit="h")


    # Drop invalid timestamps
    df = df.dropna(subset=["datetime"])

    # Remove duplicates
    df = df.drop_duplicates()

    # Sort by time (important for time series analysis)
    df = df.sort_values("datetime", ascending=False)

    df = df.reset_index(drop=True)

    return df


if __name__ == "__main__":
    from load_data import load_raw_data

    df = load_raw_data()
    clean_df = clean_data(df)
    print(clean_df["datetime"].dtype)

    print(clean_df.head())
    print(f"Shape: {clean_df.shape}")