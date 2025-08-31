from data_loader import load_districts, load_population_raster, load_ndvi_raster
from metrics import get_modis_lst, get_mean_temp, calculate_population_density, calculate_ndvi
from interventions import generate_intervention
import folium

# -------------------------------
# 1. Ask user for date range
# -------------------------------
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")

# -------------------------------
# 2. Load districts
# -------------------------------
gdf = load_districts()

# -------------------------------
# 3. MODIS LST
# -------------------------------
modis = get_modis_lst(start_date, end_date)
gdf['mean_temp'] = gdf.geometry.apply(lambda geom: get_mean_temp(geom, modis))

# -------------------------------
# 4. Population and NDVI
# -------------------------------
pop_raster_path = "population.tif"
ndvi_raster_path = "ndvi.tif"

gdf = calculate_population_density(gdf, pop_raster_path)
gdf = calculate_ndvi(gdf, ndvi_raster_path)

# -------------------------------
# 5. Generate interventions
# -------------------------------
top_hotspots = gdf.sort_values(by='mean_temp', ascending=False).head(3)
top_hotspots['intervention'] = top_hotspots.apply(
    lambda row: generate_intervention(row['district_name'], row['mean_temp']), axis=1
)

for _, row in top_hotspots.iterrows():
    print(f"{row['district_name']}: {row['intervention']}")

# -------------------------------
# 6. Save GeoJSON
# -------------------------------
gdf.to_file("dubai_districts.geojson", driver="GeoJSON")
print("Saved GeoJSON as 'dubai_districts.geojson'.")

# -------------------------------
# 7. Interactive map
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

m.save("dubai_districts_map.html")
print("Interactive map saved as 'dubai_districts_map.html'.")





