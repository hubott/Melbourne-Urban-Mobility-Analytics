# app/app.py

import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Urban Mobility Dashboard", layout="wide")


# --- Fix import path ---
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.load_data import load_raw_data
from src.clean_data import clean_data
from src.features import prepare_features, merge_weather
from src.weather_data import load_weather_data


# --- Load data ---
@st.cache_data
def get_data():
    df = pd.read_parquet("data/processed.parquet")
    heat_df = pd.read_parquet("data/heatmap.parquet")
    sensor_map = pd.read_csv("data/sensor_locations.csv")
    df = df.merge(sensor_map, on="sensor_name", how="left")
    heat_df = heat_df.merge(sensor_map, on="sensor_name", how="left")
    df["location_name"] = df["location_name"].fillna(df["sensor_name"])
    heat_df["location_name"] = heat_df["location_name"].fillna(heat_df["sensor_name"])
    return df, heat_df

df, heat_df = get_data()

@st.cache_data
def get_hourly_heatmap(df):
    return (
        df.groupby(["location_name", "hour", "lat", "lon"])["total_of_directions"]
        .mean()
        .reset_index()
    )






st.title("🚶 Melbourne Urban Mobility Insights")


top_locations = (
    df.groupby("location_name")["total_of_directions"]
    .mean()
    .sort_values(ascending=False)
    .index
    .tolist()   # 🔥 THIS FIXES IT
)

# --- Sensor selection ---
st.sidebar.subheader("📍 Locations")

sensor_options = top_locations

# --- Init state ---
if "selected_sensors" not in st.session_state:
    st.session_state.selected_sensors = top_locations[:5]

# --- Buttons ---
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("Select All"):
        st.session_state.selected_sensors = top_locations

with col2:
    if st.button("Clear All"):
        st.session_state.selected_sensors = []

# --- IMPORTANT: DO NOT use default ---
selected_sensor = st.sidebar.multiselect(
    "Focus on Locations",
    options=top_locations,
    key="selected_sensors"   # 🔥 session_state IS the source of truth
)


if selected_sensor:
    df_filtered = df[df["location_name"].isin(selected_sensor)]
else:
    df_filtered = df.copy()

# --- KPI SECTION ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", len(df_filtered))

with col2:
    st.metric("Avg Daily Traffic", int(df_filtered["total_of_directions"].mean()))

with col3:
    st.metric("Sensors", df_filtered["location_name"].nunique())

# --- HOURLY PATTERN ---
st.subheader("📊 Hourly Traffic Pattern")

hourly = df_filtered.groupby(df_filtered["datetime"].dt.hour)["total_of_directions"].mean()

st.line_chart(hourly)


# --- WEEKDAY VS WEEKEND ---
st.subheader("📅 Weekday vs Weekend")

mean_per_record = df_filtered.groupby(df_filtered["is_weekend"])["total_of_directions"].mean()
mean_per_record.index = mean_per_record.index.map({False: "Weekdays", True: "Weekend"})

st.bar_chart(mean_per_record)




df_filtered["day_of_week"] = df_filtered["datetime"].dt.day_name()
df_filtered["hour"] = df_filtered["datetime"].dt.hour

# Multi-select days
selected_days = st.multiselect(
    "Select Days of Week",
    options=df_filtered["day_of_week"].unique(),
    default=["Monday", "Tuesday"]
)

# Filter dataset
filtered = df_filtered[df_filtered["day_of_week"].isin(selected_days)]

# Group by day + hour
hourly_pattern = (
    filtered
    .groupby(["day_of_week", "hour"])["total_of_directions"]
    .mean()
    .reset_index()
)

# Pivot for plotting
pivot_df = hourly_pattern.pivot(
    index="hour",
    columns="day_of_week",
    values="total_of_directions"
)

# Plot
st.subheader("📊 Hourly Patterns by Selected Days")
st.line_chart(pivot_df)


st.subheader("🌡️ Temperature Impact on Pedestrian Activity")

# Ensure clean numeric values
df_temp = df_filtered.dropna(subset=["temperature_2m"])

bins = [-10, 0, 5, 10, 15, 20, 25, 35]
labels = [
    "Below 0°C",
    "0–5°C",
    "5–10°C",
    "10–15°C",
    "15–20°C",
    "20–25°C",
    "25°C+"
]

df_temp["temp_bin"] = pd.cut(
    df_temp["temperature_2m"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

temp_analysis = df_temp.groupby("temp_bin")["total_of_directions"].mean()
temp_df = temp_analysis.reset_index()
temp_df.columns = ["temp_bin", "avg_count"]

fig = px.bar(
    temp_df,
    x="temp_bin",
    y="avg_count",
    labels={
        "temp_bin": "Temperature Range (°C)",
        "avg_count": "Average Pedestrian Count"
    },
    title="Impact of Temperature on Pedestrian Activity"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🌧️ Rain Impact on Pedestrian Activity")

df_rain = df_filtered.dropna(subset=["precipitation"])

df_rain["rain_status"] = df_rain["precipitation"].apply(
    lambda x: "Rain" if x > 0 else "No Rain"
)

rain_analysis = df_rain.groupby("rain_status")["total_of_directions"].mean().reset_index()

fig = px.bar(
    rain_analysis,
    x="rain_status",
    y="total_of_directions",
    labels={
        "rain_status": "Weather Condition",
        "total_of_directions": "Average Pedestrian Count"
    },
    title="Impact of Rain on Pedestrian Activity"
)

st.plotly_chart(fig, use_container_width=True)





heat_hourly_df = get_hourly_heatmap(df)
heat_hourly_df = heat_hourly_df.sort_values("hour")




st.subheader("📍 Pedestrian Traffic by Hour")
hour_range = st.slider(
    "Select Hour Range",
    min_value=0,
    max_value=23,
    value=(8, 18)
)

heat_filtered = heat_hourly_df[
    (heat_hourly_df["hour"] >= hour_range[0]) &
    (heat_hourly_df["hour"] <= hour_range[1])
]

heat_filtered = (
    heat_filtered
    .groupby(["location_name", "lat", "lon"])["total_of_directions"]
    .mean()
    .reset_index()
)

color_min = heat_hourly_df["total_of_directions"].min()
color_max = heat_hourly_df["total_of_directions"].max()

fig = px.scatter_mapbox(
    heat_filtered,
    lat="lat",
    lon="lon",
    size="total_of_directions",
    color="total_of_directions",
    size_max=20,
    color_continuous_scale="Viridis",
    range_color=[color_min, color_max],
    center=dict(lat=-37.8136, lon=144.9631),
    zoom=12,
    mapbox_style="carto-positron",
    hover_name="location_name",
    hover_data={
        "lat": False,
        "lon": False,
        "total_of_directions": ":.0f"
    }
)
fig.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>Avg Count: %{marker.color:.0f}<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True)
st.caption("Color scale is consistent across all time periods for accurate comparison.")


top5 = (
    heat_filtered
    .sort_values("total_of_directions", ascending=False)
    .head(5)
    .reset_index(drop=True)
)

top5_display = top5[["location_name", "total_of_directions"]].copy()

top5_display.columns = ["Location", "Avg Pedestrian Count/hr"]

# Add ranking column
top5_display.insert(0, "Rank", range(1, len(top5_display) + 1))

st.subheader("🏆 Busiest Locations")

st.dataframe(top5_display, use_container_width=True)



# --- INSIGHTS SECTION ---
st.subheader("🧠 Key Insights")

st.markdown("""
- Peak traffic occurs during commuter hours (morning and evening)
- Certain sensors consistently show higher pedestrian volumes
- Weekend patterns differ significantly from weekdays
""")