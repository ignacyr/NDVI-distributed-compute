import rasterio
import numpy as np
from time import time
import json
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=["POST"])
def calculate_ndvi():
    start = time()
    chunk = json.loads(request.json)
    response = {"data": []}
    for d in chunk["data"]:
        # Change Windows file paths to Linux file paths
        path_red = d['path_red'][3:].replace("\\", "/")
        path_nir = d['path_nir'][3:].replace("\\", "/")

        # Read red and nir bands from file
        start_read = time()
        with rasterio.open(path_red) as tif:
            width = tif.width
            height = tif.height
            crs = tif.crs
            transform = tif.transform
            band_red = tif.read(1)
        with rasterio.open(path_nir) as tif:
            band_nir = tif.read(1)
        end_read = time()
        read_time = end_read - start_read

        # Allow division by zero
        np.seterr(divide='ignore', invalid='ignore')

        # Calculate NDVI
        start_ndvi = time()
        ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)

        # ndvi[ndvi == float('inf') or ndvi == float('+inf') or ndvi == float('-inf')] = 0.0
        # if np.nansum(ndvi) is not None:
        #     total_ndvi = np.nansum(ndvi)
        # else:
        #     total_ndvi = 0.0
        # if np.nanmean(ndvi) is not None:
        #     avg_ndvi = np.nanmean(ndvi)
        # else:
        #     avg_ndvi = 0.0

        total_ndvi = 0.0
        for row in ndvi:
            for el in row:
                if el > 0.0 and el != float('inf'):
                    total_ndvi += el

        end_ndvi = time()
        ndvi_calc_time = end_ndvi - start_ndvi

        # Saving/writing to file
        start_write = time()
        path_ndvi = path_red[:-50] + "NDVI.TIF"
        with rasterio.open(path_ndvi, 'w', driver='Gtiff', width=width, height=height, count=1,
                           crs=crs, transform=transform, dtype='float64') as tif:
            tif.write(ndvi, 1)
        end_write = time()
        write_time = end_write - start_write

        end = time()
        total_image_proc_time = end - start

        response["data"].append({"total_image_proc_time": total_image_proc_time, "total_ndvi": total_ndvi, "image": path_red[46:50],
                                 "ndvi_calc_time": ndvi_calc_time, "read_time": read_time, "write_time": write_time})
                                 # "avg_ndvi": avg_ndvi})
    return json.dumps(response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


