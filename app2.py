import streamlit as st
import geopandas as gpd
import ee
from google.oauth2 import service_account
from data_loader import load_districts
from metrics import get_mean_temp, calculate_ndvi, calculate_population_density
from datetime import datetime

st.title("Heat Analysis for Dubai Districts")

# -------------------------------
# Initialize Earth Engine
try:
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["google_service_account"]
    )
    ee.Initialize(credentials)
except Exception as e:
    st.warning(f"Earth Engine not initialized: {e}")

# -------------------------------
# User inputs
start_date = st.text_input("Enter start date (YYYY-MM-DD)")
end_date = st.text_input("Enter end date (YYYY-MM-DD)")

metric = st.selectbox("Select metric to analyze", ["Mean Temperature", "NDVI", "Population Density"])

# Load districts
gdf = load_districts()
district_names = gdf['district_name'].tolist()
district_choice = st.selectbox("Select district", ["Select..."] + district_names)

# -------------------------------
# Compute metric
if start_date and end_date and district_choice != "Select...":
    district_geom = gdf[gdf['district_name'] == district_choice].geometry.values[0]

    try:
        if metric == "Mean Temperature":
            value = get_mean_temp(district_geom, start_date, end_date)
            st.write(f"Mean Temperature for {district_choice}: {value if value else 'No data'} °C")

        elif metric == "Population Density":
            value = calculate_population_density(district_geom)
            st.write(f"Population Density for {district_choice}: {int(value) if value else 'No data'} people/km²")

        elif metric == "NDVI":
            value = calculate_ndvi(district_geom, start_date, end_date)
            st.write(f"NDVI for {district_choice}: {value if value else 'No data'}")

    except Exception as e:
        st.error(f"Error computing metric: {e}")


