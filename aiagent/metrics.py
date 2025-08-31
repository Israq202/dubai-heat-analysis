import ee
import rasterio
import numpy as np
from rasterio import features
from shapely.geometry import Polygon, MultiPolygon

# Initialize Earth Engine
ee.Initialize()

# -----------------------------
# MODIS LST
# -----------------------------
def get_modis_lst(start_date, end_date):
    """Fetch MODIS LST mean for given date range."""
    try:
        collection = ee.ImageCollection('MODIS/061/MOD11A1') \
            .filterDate(start_date, end_date) \
            .select('LST_Day_1km') \
            .mean() \
            .multiply(0.02) \
            .subtract(273.15)  # Kelvin to Celsius
        return collection
    except Exception as e:
        raise RuntimeError(f"Error fetching MODIS data: {e}")

def get_mean_temp(geom, modis_collection):
    """Compute mean LST for a given geometry."""
    try:
        if isinstance(geom, Polygon):
            coords = list(geom.exterior.coords)
            ee_geom = ee.Geometry.Polygon(coords)
        elif isinstance(geom, MultiPolygon):
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
    except Exception as e:
        raise RuntimeError(f"Error computing mean temperature: {e}")


# -----------------------------
# Population Density
# -----------------------------
import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np

def calculate_population_density(geom, pop_raster_path):
    """
    Calculate population density (people/km²) for a single polygon geometry.
    
    geom: shapely Polygon or MultiPolygon
    pop_raster_path: path to the population raster (GeoTIFF)
    """
    # Ensure geometry is in GeoJSON-like mapping for rasterio.mask
    if geom.geom_type == 'Polygon':
        geoms = [geom.__geo_interface__]
    elif geom.geom_type == 'MultiPolygon':
        geoms = [poly.__geo_interface__ for poly in geom.geoms]
    else:
        raise ValueError("Geometry must be Polygon or MultiPolygon")

    with rasterio.open(pop_raster_path) as src:
        # Ensure CRS match
        if src.crs.to_string() != "EPSG:4326":
            raise ValueError("Population raster must be in EPSG:4326 CRS")

        # Mask raster to the district polygon
        out_image, out_transform = mask(src, geoms, crop=True)
        out_image = out_image[0]  # single band

        # Ignore nodata pixels
        nodata = src.nodata
        if nodata is not None:
            out_image = np.where(out_image == nodata, 0, out_image)

        # Total population in the polygon
        total_population = np.sum(out_image)

        # Calculate area of polygon in km² using approximate conversion for WGS84
        # 1 degree ≈ 111 km, better to project to meters for exact area
        from shapely.ops import transform
        import pyproj

        project = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True).transform
        geom_m = transform(project, geom)
        area_m2 = geom_m.area
        area_km2 = area_m2 / 1e6

        if area_km2 == 0:
            return None

        pop_density = total_population / area_km2
        return pop_density


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

