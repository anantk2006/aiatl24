from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from geopy.distance import geodesic
from numba import jit
import json

# Initialize FastAPI app
app = FastAPI()

# Load and preprocess the data when the app starts
cols = ['Id', 'Name', 'Date', 'Time', 'RecordID', 'Status', 'Lat', 'Lon',
        'MaxWind', 'MinPressure', '34kt_NE', '34kt_SE', '34kt_SW', '34kt_NW',
        '50kt_NE', '50kt_SE', '50kt_SW', '50kt_NW', '64kt_NE', '64kt_SE',
        '64kt_SW', '64kt_NW', 't']

dtypes = {
    'Id': 'string',
    'Name': 'string',
    'Date': 'datetime64[ns]',
    'Time': 'string',
    'RecordID': 'string',
    'Status': 'string',
    'Lat': 'float64',
    'Lon': 'float64',
    'MaxWind': 'float64',
    'MinPressure': 'float64',
    '34kt_NE': 'float64',
    '34kt_SE': 'float64',
    '34kt_SW': 'float64',
    '34kt_NW': 'float64',
    '50kt_NE': 'float64',
    '50kt_SE': 'float64',
    '50kt_SW': 'float64',
    '50kt_NW': 'float64',
    '64kt_NE': 'float64',
    '64kt_SE': 'float64',
    '64kt_SW': 'float64',
    '64kt_NW': 'float64'
}

# Read and preprocess the data
def load_data():
    data = []
    def convert_lat_lon(lat_str, lon_str):
        lat = float(lat_str[:-1])
        lon = float(lon_str[:-1])
        if lat_str.endswith('S'):
            lat = -lat
        if lon_str.endswith('W'):
            lon = -lon
        return lat, lon

    with open('hurdat2.txt', 'r') as file:
        name = ""
        id = ""
        skip = False
        for line in file:
            values = [value.strip() for value in line.strip().split(",")]
            if len(values) < 5:
                name = values[1]
                id = values[0]
                skip = int(values[2]) < 4
                continue
            if skip: continue
            lat, lon = convert_lat_lon(values[4], values[5])
            row = [id, name] + values[:4] + [lat, lon] + values[6:]
            data.append(row)

    df = pd.DataFrame.from_records(data, columns=cols).astype(dtypes)
    df['Date'] = pd.to_datetime(df['Date'])
    cutoff_date = datetime.now() - timedelta(days=15 * 365)
    df = df[df['Date'] >= cutoff_date]

    df['MaxRadius_km'] = df.apply(calculate_max_radius, axis=1)
    return df

# Calculate the maximum radius in kilometers
def calculate_max_radius(row):
    wind_radii = [
        row['34kt_NE'], row['34kt_SE'], row['34kt_SW'], row['34kt_NW'],
        row['50kt_NE'], row['50kt_SE'], row['50kt_SW'], row['50kt_NW'],
        row['64kt_NE'], row['64kt_SE'], row['64kt_SW'], row['64kt_NW']
    ]
    mx = max(wind_radii)
    if mx < 10:
        mx = 260.
    return mx * 1.852

# Haversine function to calculate distance
@jit(nopython=True)
def haversine(lat1, lon1, lat2, lon2):
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    r = 6371.0
    return r * c

# Find hurricanes that intersect with a given location
def find_intersecting_hurricanes(df, target_lat, target_lon):
    intersecting_hurricanes = []

    for _, row in df.iterrows():
        distance = haversine(row['Lat'], row['Lon'], target_lat, target_lon)
        if distance <= row['MaxRadius_km']:
            row['Distance_km'] = distance
            intersecting_hurricanes.append(row)

    return pd.DataFrame(intersecting_hurricanes)

# Input model for the API
class LocationInput(BaseModel):
    lat: float
    lng: float

# Load data at startup
df = load_data()

# API endpoint to find hurricanes
@app.post("/find_hurricanes")
def find_hurricanes(location: LocationInput):
    target_lat = location.lat
    target_lon = location.lng

    intersecting_df = find_intersecting_hurricanes(df, target_lat, target_lon)
    top_5_ids = (
        intersecting_df.groupby('Id')
        .agg(Name=('Name', 'max'), Min_Distance_km=('Distance_km', 'min'), Max_Wind=('MaxWind', 'max'))
        .sort_values(by='Max_Wind')
        .head(5)
        .index.tolist()
    )

    matching_rows_df = df[df['Id'].isin(top_5_ids)]
    hurricanes_json = {
        hurricane_id: {
            'name': group['Name'].iloc[0],
            'maxSpeed': group['MaxWind'].max(),
            'color': 'red' if group['MaxWind'].max() >= 130 else 'orange' if group['MaxWind'].max() >= 90 else 'yellow',
            'points': [{'lat': row['Lat'], 'lng': row['Lon'], 'r': row['MaxRadius_km']} for _, row in group.iterrows()]
        }
        for hurricane_id, group in matching_rows_df.groupby('Id')
    }

    return hurricanes_json
