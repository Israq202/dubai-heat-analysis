import geopandas as gpd
import rasterio

def load_districts():
    return gpd.read_file("districts.geojson")  # your districts GeoJSON

def load_population_raster():
    return rasterio.open("population.tif")  # your population raster

def load_ndvi_raster():
    return rasterio.open("ndvi.tif")  # your NDVI raster

