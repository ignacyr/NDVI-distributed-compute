import rasterio
from matplotlib import pyplot as plt
import numpy as np
from time import time
import sys


path_red = "D:\\\\SatelliteImagesBIGDATA\\2022\\LC09_L2SP_190024_20220721_20220723_02_T1_SR_B4.TIF"
path_nir = "D:\\\\SatelliteImagesBIGDATA\\2022\\LC09_L2SP_190024_20220721_20220723_02_T1_SR_B5.TIF"

with rasterio.open(path_red) as tif:
    band_red = tif.read(1)
    plt.imshow(band_red, cmap='pink')
    plt.show()

with rasterio.open(path_nir) as tif:
    band_nir = tif.read(1)
    plt.imshow(band_nir, cmap='pink')
    plt.show()

# Allow division by zero
np.seterr(divide='ignore', invalid='ignore')

# Calculate NDVI
start = time()
ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)
end = time()

# print(ndvi)
plt.imshow(ndvi, cmap='summer')
plt.show()
summ = 0.0  # suma wartości każdego pixela (suma ndvi)
for row in ndvi:
    for el in row:
        if el > 0.0:
            summ += el
print(summ)

print(end - start)

