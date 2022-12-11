import os
from time import sleep


for i in range(1, 16):
    os.system(f"python master/master.py {i}")
    sleep(10)


