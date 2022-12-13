import json
import os
import random
import asyncio
from time import time, sleep
import sys
from statistics import mean

import aiohttp

path = 'D:\\\\SatelliteImagesBIGDATA\\'
containers = int(sys.argv[1])
ram_limit = 1.5

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
chunks = [images[i::containers] for i in range(containers)]

for i in range(containers):
    command = f"docker run --rm -d -p 5{i:03d}:5000 " \
              f"--mount type=bind,source=D:\\SatelliteImagesBIGDATA,target=/SatelliteImagesBIGDATA " \
              f"--cpus=1 " \
              f"--memory={ram_limit}g " \
              f"ndvi-compute-executor"
    print(command)
    output = os.system(command)

# Wait for containers initialization
sleep(5)


async def get_ndvi(session, i, chunk):
    print('Starting job ' + str(i))
    async with session.post(url=f'http://127.0.0.1:5{i:03d}', json=json.dumps({"data": chunk})) as response:
        print('Job ' + str(i) + ' finalized')
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(get_ndvi(session, i, chunk)) for i, chunk in enumerate(chunks)]
        results = await asyncio.gather(*tasks)
        return results


print(f"Number of containers: {len(chunks)}")
print("Starting app...")
start = time()
ndvi_results = asyncio.run(main())
end = time()
total_time = end - start

total_image_proc_time = []
ndvi_calc_time = []
read_time = []
write_time = []
for r in ndvi_results:
    r = json.loads(r)
    for im in r["data"]:
        total_image_proc_time.append(im["total_image_proc_time"])
        ndvi_calc_time.append(im["ndvi_calc_time"])
        read_time.append(im["read_time"])
        write_time.append(im["write_time"])
        # print(im["avg_ndvi"], im["total_ndvi"])


print(f"Total processing time: {total_time}")

with open("measurements.csv", "a") as f:
    f.write(f"{containers},{ram_limit},{total_time},{mean(total_image_proc_time)},"
            f"{mean(ndvi_calc_time)},{mean(read_time)},{mean(write_time)}\n")

# ERROR 125
# os.system("docker stop $(docker ps -aq)")
# os.system("docker rm $(docker ps -aq)")






