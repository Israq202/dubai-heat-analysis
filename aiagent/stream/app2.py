import streamlit as st
from data_loader import load_districts, load_population_raster, load_ndvi_raster
from metrics import get_modis_lst, get_mean_temp, calculate_population_density, calculate_ndvi
from interventions import generate_intervention

st.title("Heat Analysis for Dubai Districts")

# User inputs
start_date = st.text_input("Enter start date (YYYY-MM-DD)")
end_date = st.text_input("Enter end date (YYYY-MM-DD)")
metric = st.selectbox("Select metric to analyze", ["Mean Temperature", "NDVI", "Population Density"])

# Load districts
try:
    gdf = load_districts()
except Exception as e:
    st.error(f"Error loading districts: {e}")
    st.stop()

district_choice = st.selectbox("Select district", ["Select..."] + gdf['district_name'].tolist())

# Only proceed if valid inputs
if start_date and end_date and district_choice != "Select...":
    district_geom = gdf[gdf['district_name'] == district_choice].geometry.values[0]

    try:
        if metric == "Mean Temperature":
            modis = get_modis_lst(start_date, end_date)
            value = get_mean_temp(district_geom, modis)
        elif metric == "Population Density":
            raster = load_population_raster()
            value = calculate_population_density(district_geom, raster)
        elif metric == "NDVI":
            raster = load_ndvi_raster()
            value = calculate_ndvi(district_geom, raster)
        else:
            value = None

        st.write(f"{metric} for {district_choice}: {value if value is not None else 'No data'}")
        st.write("Recommended intervention:", generate_intervention(district_choice, metric, value))

    except Exception as e:
        st.error(f"Error computing metric: {e}")


