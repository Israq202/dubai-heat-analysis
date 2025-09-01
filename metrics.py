import ee

def get_mean_temp(district_geom, start_date, end_date):
    try:
        modis = ee.ImageCollection("MODIS/006/MOD11A1") \
                    .filterDate(start_date, end_date) \
                    .select("LST_Day_1km") \
                    .mean()
        stats = modis.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=district_geom,
            scale=1000
        ).getInfo()
        value = stats.get("LST_Day_1km")
        if value is not None:
            return value * 0.02 - 273.15  # Convert MODIS LST to °C
        return None
    except Exception as e:
        return f"Error fetching MODIS data: {e}"

def calculate_ndvi(district_geom, start_date, end_date):
    try:
        ndvi = ee.ImageCollection("MODIS/006/MOD13A2") \
                    .filterDate(start_date, end_date) \
                    .select("NDVI") \
                    .mean()
        stats = ndvi.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=district_geom,
            scale=500
        ).getInfo()
        value = stats.get("NDVI")
        if value is not None:
            return value / 10000  # MODIS NDVI scaling
        return None
    except Exception as e:
        return f"Error fetching NDVI data: {e}"

def calculate_population_density(district_geom):
    try:
        pop = ee.ImageCollection("CIESIN/GPWv411/GPW_Population_Density").mosaic()
        stats = pop.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=district_geom,
            scale=1000
        ).getInfo()
        value = stats.get("population_density")
        return value
    except Exception as e:
        return f"Error fetching population density: {e}"
