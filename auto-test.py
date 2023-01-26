import os
from time import sleep
import sys

containers = int(sys.argv[1])
ram_limit = 1.5

for i in range(containers):
    command = f"docker run --rm -d -p 5{i:03d}:5000 " \
              f"--mount type=bind,source=C:\\SatelliteImagesBIGDATA,target=/SatelliteImagesBIGDATA " \
              f"--cpus=1 " \
              f"--memory={ram_limit}g " \
              f"ndvi-compute-executor"
    print(command)
    output = os.system(command)

# Wait for containers initialization
sleep(5)

for i in range(1, containers+1):
    os.system(f"python master/master.py {i} 1")
    sleep(10)


