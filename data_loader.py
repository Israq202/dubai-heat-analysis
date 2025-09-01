import geopandas as gpd

def load_districts():
    # Load districts from local GeoJSON
    gdf = gpd.read_file("districts.geojson")
    return gdf


