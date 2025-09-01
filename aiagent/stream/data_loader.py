import os
import geopandas as gpd
import rasterio

BASE_DIR = os.path.dirname(__file__)

def load_districts():
    """Load Dubai districts from GeoJSON."""
    districts_file = os.path.join(BASE_DIR, "dubai_districts.geojson")
    if not os.path.exists(districts_file):
        raise FileNotFoundError("Districts GeoJSON not found in repo.")
    return gpd.read_file(districts_file)

def load_population_raster():
    """Load population raster from repo."""
    raster_file = os.path.join(BASE_DIR, "population.tif")
    if not os.path.exists(raster_file):
        raise FileNotFoundError("Population raster not found in repo.")
    return rasterio.open(raster_file)

def load_ndvi_raster():
    """Load NDVI raster from repo."""
    raster_file = os.path.join(BASE_DIR, "ndvi.tif")
    if not os.path.exists(raster_file):
        raise FileNotFoundError("NDVI raster not found in repo.")
    return rasterio.open(raster_file)

