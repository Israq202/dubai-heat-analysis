import streamlit as st
import geopandas as gpd
import ee
from data_loader import load_districts, load_population_raster, load_ndvi_raster
from metrics import get_mean_temp, calculate_population_density, calculate_ndvi
from datetime import datetime
from google.oauth2 import service_account

st.title("Heat Analysis for Dubai Districts")

# -------------------------------
# Initialize Earth Engine
# -------------------------------
try:
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["google_service_account"]
    )
    ee.Initialize(credentials)
except Exception as e:
    st.warning(f"Earth Engine not initialized: {e}")

# -------------------------------
# User Inputs
# -------------------------------
start_date = st.text_input("Enter start date (YYYY-MM-DD)")
end_date = st.text_input("Enter end date (YYYY-MM-DD)")
metric = st.selectbox("Select metric to analyze", ["Mean Temperature", "NDVI", "Population Density"])

# Load districts
gdf = load_districts()
district_names = gdf['district_name'].tolist()
district_choice = st.selectbox("Select district", ["Select..."] + district_names)

# -------------------------------
# Compute Metric
# -------------------------------
if start_date and end_date and district_choice != "Select...":
    district_geom = gdf[gdf['district_name'] == district_choice].geometry.values[0]

    try:
        if metric == "Mean Temperature":
            # Only compute if Earth Engine initialized
            if "ee" in globals() and ee.data._credentials:
                modis = get_mean_temp(district_geom, start_date, end_date)
                st.write(f"Mean Temperature for {district_choice}: {modis if modis else 'No data'} °C")
            else:
                st.write("Earth Engine not initialized. Cannot compute temperature.")

        elif metric == "Population Density":
            raster = load_population_raster()
            value = calculate_population_density(district_geom, raster)
            st.write(f"Population Density for {district_choice}: {int(value) if value else 'No data'} people/km²")

        elif metric == "NDVI":
            raster = load_ndvi_raster()
            value = calculate_ndvi(district_geom, raster)
            st.write(f"NDVI for {district_choice}: {value if value else 'No data'}")

    except Exception as e:
        st.error(f"Error computing metric: {e}")


