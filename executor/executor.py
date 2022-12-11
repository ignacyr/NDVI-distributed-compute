import rasterio
import numpy as np
from time import time
import json
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=["POST"])
def calculate_ndvi():
    start = time()
    # print(request.json)
    chunk = json.loads(request.json)
    response = ""
    for d in chunk["data"]:
        path_red = d['path_red'][3:].replace("\\", "/")
        path_nir = d['path_nir'][3:].replace("\\", "/")

        with rasterio.open(path_red) as tif:
            width = tif.width
            height = tif.height
            crs = tif.crs
            transform = tif.transform
            band_red = tif.read(1)

        with rasterio.open(path_nir) as tif:
            band_nir = tif.read(1)

        # Allow division by zero
        np.seterr(divide='ignore', invalid='ignore')

        # Calculate NDVI
        ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)

        summ = 0.0
        for row in ndvi:
            for el in row:
                if el > 0.0 and el != float('inf'):
                    summ += el
        # print(f"Total NDVI: {summ}")

        path_ndvi = path_red[:-50] + "NDVI.TIF"
        with rasterio.open(path_ndvi, 'w', driver='Gtiff', width=width, height=height, count=1,
                           crs=crs, transform=transform, dtype='float64') as tif:
            tif.write(ndvi, 1)

        with rasterio.open(path_ndvi) as tif:
            ndvi = tif.read(1)
            # plt.imshow(band_nir, cmap='summer')
            # plt.show()

        end = time()
        # print(f"Time: {end - start}")
        response += f"Time: {end - start}\nTotal NDVI: {summ}\nImage {path_red}"
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


