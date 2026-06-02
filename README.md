# Melbourne Pedestrian Activity Analysis

## Overview

This project analyses pedestrian traffic patterns across Melbourne CBD using data from the City of Melbourne Pedestrian Counting System.

The analysis explores:

- Daily and hourly pedestrian activity patterns
- Differences between sensor locations
- Peak activity periods
- Spatial distribution of pedestrian traffic

An interactive Streamlit dashboard was developed to allow users to explore trends and visualisations.

## Live Dashboard

View the deployed dashboard here:

[Interactive Dashboard](https://melbourne-urban-mobility-analytics.streamlit.app)

## Dataset

Source: City of Melbourne Open Data

The dataset contains pedestrian counts collected from sensors located throughout Melbourne CBD.

The original raw dataset is not included in this repository due to its size. Processed datasets used by the dashboard are provided in Parquet format.

## Features

- Interactive sensor selection
- Hourly pedestrian trend analysis
- Comparison of busiest sensors
- Heatmap visualisations
- Responsive Streamlit dashboard

## Technologies

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- PyArrow

## Repository Structure

## Repository Structure

```
.
├── app/
│   └── app.py                  # Streamlit dashboard entry point
│
├── data/
│   ├── processed.parquet      # Main cleaned dataset used by the app
│   ├── heatmap.parquet        # Precomputed heatmap data
│   └── sensor_mapping.csv     # Maps sensor IDs to human-readable names
│
├── notebooks/
│   └── eda.ipynb         # Exploratory data analysis & experimentation
│
├── scripts/
│   └── preprocess.py          # Orchestrates full data preprocessing pipeline
│
├── src/
│   ├── clean_data.py
│   ├── features.py
│   ├── load_data.py
│   └── weather_data.py
│
├── requirements.txt
├── README.md
└── .gitignore
```


## Running Locally

Clone the repository:

```bash
git clone <repo-url>
cd <repo-name>

pip install -r requirements.txt

streamlit run app/app.py

