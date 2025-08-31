import rasterio

ndvi_path = "ndvi.tif"  # make sure this path is correct

# Open the raster
with rasterio.open(ndvi_path) as src:
    print("NDVI Raster Info:")
    print(f"Width: {src.width}, Height: {src.height}")
    print(f"Bounds: {src.bounds}")
    print(f"CRS: {src.crs}")
    print(f"Number of bands: {src.count}")
    
    # Read the first band
    band1 = src.read(1)
    print(f"Min NDVI value: {band1.min()}, Max NDVI value: {band1.max()}")
with rasterio.open("ndvi.tif") as src:
    band1 = src.read(1)
    print(f"Min NDVI value: {band1.min()}, Max NDVI value: {band1.max()}")
