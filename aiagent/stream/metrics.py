import rasterio
from rasterio.mask import mask
import numpy as np
import ee

# Initialize Earth Engine if needed
try:
    ee.Initialize()
except Exception:
    pass

def get_modis_lst(start_date, end_date):
    """Fetch MODIS LST for given date range."""
    try:
        collection = ee.ImageCollection('MODIS/061/MOD11A1') \
                      .filterDate(start_date, end_date) \
                      .select('LST_Day_1km') \
                      .mean() \
                      .multiply(0.02).subtract(273.15)
        return collection
    except Exception as e:
        raise ValueError(f"Error fetching MODIS data: {e}")

def get_mean_temp(geom, modis_collection):
    """Compute mean temperature for a district."""
    try:
        if geom.geom_type == 'Polygon':
            coords = list(geom.exterior.coords)
            ee_geom = ee.Geometry.Polygon(coords)
        elif geom.geom_type == 'MultiPolygon':
            coords = [list(p.exterior.coords) for p in geom.geoms]
            ee_geom = ee.Geometry.MultiPolygon(coords)
        else:
            return None

        mean_dict = modis_collection.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=ee_geom,
            scale=1000
        ).getInfo()
        return mean_dict.get('LST_Day_1km', None)
    except Exception:
        return None

def calculate_population_density(geom, raster):
    """Compute population density for a district."""
    try:
        out_image, out_transform = mask(raster, [geom], crop=True)
        data = out_image[0]
        data = data[data >= 0]  # filter out nodata
        area_km2 = data.size * (raster.res[0] * raster.res[1]) / 1e6
        total_pop = np.sum(data)
        density = total_pop / area_km2 if area_km2 > 0 else None
        return density
    except Exception:
        return None

def calculate_ndvi(geom, raster):
    """Compute NDVI for a district."""
    try:
        out_image, out_transform = mask(raster, [geom], crop=True)
        data = out_image[0]
        data = data[data >= 0]
        return float(np.mean(data)) if data.size > 0 else None
    except Exception:
        return None



# -----------------------------
# NDVI
# -----------------------------
def calculate_ndvi(geom, ndvi_raster_path):
    """Compute mean NDVI for a given geometry."""
    try:
        with rasterio.open(ndvi_raster_path) as src:
            mask = features.geometry_mask([geom], transform=src.transform,
                                          invert=True, out_shape=(src.height, src.width))
            data = src.read(1, masked=True)
            ndvi_mean = np.mean(data[mask])
        return ndvi_mean
    except Exception as e:
        raise RuntimeError(f"Error computing NDVI: {e}")

