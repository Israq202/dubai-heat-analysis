import streamlit as st
import geopandas as gpd
import ee
from google.oauth2 import service_account
from datetime import datetime
from data_loader import load_districts, load_population_raster, load_ndvi_raster
from metrics import get_mean_temp, calculate_population_density, calculate_ndvi

st.title("Heat Analysis for Dubai Districts")

# -------------------------------
# Initialize Earth Engine
try:
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["google_service_account"],
        scopes=["https://www.googleapis.com/auth/earthengine"]
    )
    ee.Initialize(credentials, st.secrets["google_service_account"]["client_email"])
    st.success("Earth Engine initialized successfully!")
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
# Only proceed if valid inputs
if start_date and end_date and district_choice != "Select...":
    district_geom = gdf[gdf['district_name'] == district_choice].geometry.values[0]

    try:
        if metric == "Mean Temperature":
            # Earth Engine MODIS LST dynamic calculation
            value = get_mean_temp(district_geom, start_date, end_date)
            st.write(f"Mean Temperature for {district_choice}: {value if value else 'No data'} °C")

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


