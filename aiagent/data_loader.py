import geopandas as gpd
import rasterio
from pathlib import Path

def load_districts():
    # Load from GeoJSON
    return gpd.read_file("dubai_districts.geojson")

def load_population_raster():
    pop_path = Path("population.tif")
    if not pop_path.exists():
        raise FileNotFoundError("population.tif not found. Please download or generate it.")
    return pop_path

def load_ndvi_raster():
    ndvi_path = Path("ndvi.tif")
    if not ndvi_path.exists():
        raise FileNotFoundError("ndvi.tif not found. Please download or generate it.")
    return ndvi_path


