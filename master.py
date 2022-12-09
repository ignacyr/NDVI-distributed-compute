import json
import os
import random

import requests

path = 'D:\\\\SatelliteImagesBIGDATA\\'
cores = 5

images = []

for d in os.listdir(path):
    p_red, p_nir = "", ""
    for f in os.listdir(path + d):
        if f[-6:] == "B4.TIF":
            p_red = path + d + '\\' + f
        elif f[-6:] == "B5.TIF":
            p_nir = path + d + '\\' + f
    images.append({
        "path_red": p_red,
        "path_nir": p_nir,
        "size": os.path.getsize(p_red) + os.path.getsize(p_nir)
    })

random.shuffle(images)
chunks = [images[i::cores] for i in range(cores)]


for chunk in chunks:
    print(chunk)
    response = requests.post(url="http://127.0.0.1:5000", json=json.dumps({"data": chunk}))
    print(response)
    print(response.text)







