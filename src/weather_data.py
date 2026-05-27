# src/weather_data.py

import pandas as pd
import requests


def load_weather_data(start_date="2024-01-01", end_date="2024-12-31"):
    """
    Fetch hourly weather data for Melbourne from Open-Meteo.
    """

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        "?latitude=-37.8136"
        "&longitude=144.9631"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
        "&hourly=temperature_2m,precipitation"
        "&timezone=Australia%2FSydney"
    )

    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data["hourly"])

    # convert time column to datetime
    df["datetime"] = pd.to_datetime(df["time"])

    df = df.drop(columns=["time"])

    return df


if __name__ == "__main__":
    df = load_weather_data()
    print(df.head())
    print(df.shape)