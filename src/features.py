# src/features.py

import pandas as pd


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds time-based features for analysis.
    """

    df["hour"] = df["datetime"].dt.hour
    df["day_of_week"] = df["datetime"].dt.day_name()
    df["date"] = df["datetime"].dt.date

    df["is_weekend"] = df["datetime"].dt.dayofweek >= 5

    return df


def aggregate_hourly(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates data to hourly level (useful for dashboards).
    """

    # ASSUMPTION: there is a 'count' column (adjust if needed)
    hourly = (
        df.groupby(["datetime"])
        .agg({"count": "sum"})
        .reset_index()
    )

    return hourly


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full feature pipeline.
    """

    df = add_time_features(df)
    df[["lat", "lon"]] = df["location"].str.split(",", expand=True).astype(float)
    return df

def merge_weather(pedestrian_df, weather_df):
    """
    Join weather data to pedestrian data on hourly timestamp.
    """

    pedestrian_df["datetime"] = pd.to_datetime(pedestrian_df["datetime"])
    weather_df["datetime"] = pd.to_datetime(weather_df["datetime"])

    merged = pd.merge(
        pedestrian_df,
        weather_df,
        on="datetime",
        how="left"
    )

    return merged


if __name__ == "__main__":
    from load_data import load_raw_data
    from clean_data import clean_data

    df = load_raw_data()
    df = clean_data(df)
    df = prepare_features(df)

    print(df.head())