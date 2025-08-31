import osmnx as ox
import geopandas as gpd
import ee
import folium
from pathlib import Path

# -------------------------------
# 0. Initialize Earth Engine
# -------------------------------
ee.Initialize()

# -------------------------------
# 1. Load districts from OSM
# -------------------------------
gdf = ox.features_from_xml("ddistricts.osm", tags={'admin_level':'10'})
gdf = gdf[gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])].copy()
gdf = gdf.reset_index(drop=True)

# Check for district name
if 'name' in gdf.columns:
    gdf['district_name'] = gdf['name']
else:
    gdf['district_name'] = None

# -------------------------------
# 2. Function: Fetch MODIS LST dynamically
# -------------------------------
def get_modis_lst(start_date, end_date):
    collection = ee.ImageCollection('MODIS/061/MOD11A1') \
                  .filterDate(start_date, end_date) \
                  .select('LST_Day_1km') \
                  .mean() \
                  .multiply(0.02) \
                  .subtract(273.15)  # Convert Kelvin to Celsius
    return collection

# -------------------------------
# 3. Function: Compute mean temp per district
# -------------------------------
def get_mean_temp(geom, modis_collection):
    if geom.type == 'Polygon':
        coords = list(geom.exterior.coords)
        ee_geom = ee.Geometry.Polygon(coords)
    elif geom.type == 'MultiPolygon':
        coords = [list(poly.exterior.coords) for poly in geom.geoms]
        ee_geom = ee.Geometry.MultiPolygon(coords)
    else:
        return None
    
    mean_dict = modis_collection.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=ee_geom,
        scale=1000
    ).getInfo()
    
    return mean_dict.get('LST_Day_1km', None)

# -------------------------------
# 4. Manual intervention input
# -------------------------------
def input_intervention(district_name, mean_temp):
    print(f"\nDistrict: {district_name} | Mean Temp: {mean_temp:.1f}°C")
    intervention = input("Enter the intervention manually: ")
    return intervention.strip()

# -------------------------------
# 5. Get user input for date range
# -------------------------------
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")

modis = get_modis_lst(start_date, end_date)

# Compute mean temperature
print("Computing mean temperatures for districts...")
gdf['mean_temp'] = gdf.geometry.apply(lambda geom: get_mean_temp(geom, modis))

# -------------------------------
# 6. Enter interventions for top hotspots
# -------------------------------
top_hotspots = gdf.sort_values(by='mean_temp', ascending=False).head(3)
top_hotspots['intervention'] = top_hotspots.apply(
    lambda row: input_intervention(row['district_name'], row['mean_temp']), axis=1
)

for _, row in top_hotspots.iterrows():
    print(f"{row['district_name']}: {row['intervention']}")

# -------------------------------
# 7. Save districts to GeoJSON
# -------------------------------
gdf.to_file("dubai_districts.geojson", driver="GeoJSON")
print("Saved GeoJSON as 'dubai_districts.geojson'.")

# -------------------------------
# 8. Create interactive Folium map
# -------------------------------
m = folium.Map(location=[25.2048, 55.2708], zoom_start=11)

for _, row in gdf.iterrows():
    temp = row['mean_temp']
    color = 'blue' if temp is None else 'blue' if temp < 35 else 'orange' if temp < 40 else 'red'
    tooltip_text = f"{row['district_name']} - {temp:.1f}°C"
    if row['district_name'] in top_hotspots['district_name'].values:
        hotspot_info = top_hotspots[top_hotspots['district_name'] == row['district_name']]['intervention'].values[0]
        tooltip_text += f"\nIntervention: {hotspot_info}"

    folium.GeoJson(
        row['geometry'],
        style_function=lambda x, col=color: {
            'fillColor': col,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.5
        },
        tooltip=tooltip_text
    ).add_to(m)

# Save map
m.save("dubai_districts_map.html")
print("Interactive map saved as 'dubai_districts_map.html'.")





