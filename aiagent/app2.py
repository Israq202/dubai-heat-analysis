import streamlit as st
import geopandas as gpd
from data_loader import load_districts, load_population_raster, load_ndvi_raster
from metrics import get_modis_lst, get_mean_temp, calculate_population_density, calculate_ndvi

st.title("Heat Analysis for Dubai Districts")

# -----------------------------
# User Inputs
# -----------------------------
start_date = st.text_input("Enter start date (YYYY-MM-DD)")
end_date = st.text_input("Enter end date (YYYY-MM-DD)")
metric = st.selectbox("Select metric to analyze", ["Mean Temperature", "NDVI", "Population Density"])

# Load districts
gdf = load_districts()
district_choice = st.selectbox("Select district", ["Select..."] + gdf['district_name'].tolist())

# -----------------------------
# Perform Analysis
# -----------------------------
if start_date and end_date and district_choice != "Select...":
    district_geom = gdf[gdf['district_name'] == district_choice].geometry.values[0]

    try:
        if metric == "Mean Temperature":
            modis = get_modis_lst(start_date, end_date)
            value = get_mean_temp(district_geom, modis)
            st.write(f"Mean Temperature for {district_choice}: {value if value else 'No data'} °C")

        elif metric == "Population Density":
            pop_raster = load_population_raster()
            value = calculate_population_density(district_geom, pop_raster)
            st.write(f"Population Density for {district_choice}: {int(value) if value else 'No data'} people/km²")

        elif metric == "NDVI":
            ndvi_raster = load_ndvi_raster()
            value = calculate_ndvi(district_geom, ndvi_raster)
            st.write(f"NDVI for {district_choice}: {value if value else 'No data'}")

    except Exception as e:
        st.error(f"Error computing metric: {e}")


