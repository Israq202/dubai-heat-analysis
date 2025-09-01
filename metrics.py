import ee
import numpy as np
import rasterio
from rasterio.mask import mask

# Mean temperature via MODIS dynamically from EE
def get_mean_temp(geom, start_date, end_date):
    try:
        region = ee.Geometry.Polygon(list(geom.exterior.coords))
        dataset = ee.ImageCollection('MODIS/006/MOD11A1') \
                    .filterDate(start_date, end_date) \
                    .select('LST_Day_1km')
        mean_lst = dataset.mean().reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=1000
        )
        value = mean_lst.get('LST_Day_1km').getInfo()
        return value * 0.02 - 273.15  # scale factor to Celsius
    except Exception as e:
        raise Exception(f"Error fetching MODIS data: {e}")

# Population density from raster
def calculate_population_density(geom, raster):
    try:
        if hasattr(geom, 'geometry'):
            geom = geom.geometry
        out_image, out_transform = mask(raster, [geom], crop=True)
        arr = out_image[0]
        arr = arr[arr > 0]
        return float(np.mean(arr)) if arr.size > 0 else None
    except Exception as e:
        raise Exception(f"Error computing Population Density: {e}")

# NDVI from raster
def calculate_ndvi(geom, raster):
    try:
        if hasattr(geom, 'geometry'):
            geom = geom.geometry
        out_image, out_transform = mask(raster, [geom], crop=True)
        arr = out_image[0]
        arr = arr[arr != raster.nodata]
        return float(np.mean(arr)) if arr.size > 0 else None
    except Exception as e:
        raise Exception(f"Error computing NDVI: {e}")

