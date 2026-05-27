import pandas as pd
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from src.load_data import load_raw_data
from src.clean_data import clean_data
from src.features import prepare_features, merge_weather
from src.weather_data import load_weather_data

print("Loading raw data...")
df = load_raw_data()

print("Cleaning...")
df = clean_data(df)

print("Feature engineering...")
df = prepare_features(df)

# extract lat/lon
df[["lat", "lon"]] = df["location"].str.split(",", expand=True).astype(float)

print("Loading weather...")
df_weather = load_weather_data()

print("Merging...")
df = merge_weather(df, df_weather)

# 🔥 OPTIONAL: reduce dataset size (VERY IMPORTANT)
#df = df.sample(n=1_000_000, random_state=42)

print("Saving processed data...")
df.to_parquet("data/processed.parquet")

# precompute heatmap
heat_df = (
    df.groupby(["sensor_name", "lat", "lon"])["total_of_directions"]
    .mean()
    .reset_index()
)

heat_df.to_parquet("data/heatmap.parquet")

print("Done.")