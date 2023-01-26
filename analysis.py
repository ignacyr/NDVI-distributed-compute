import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("measurements_8.csv")
df = df.loc[df["ram_limit"] == 1.5]
df = df.groupby("containers", as_index=False).mean()
df = df.sort_values(by="containers")
df["speedup_RW"] = df["total_time"][0] / df["total_time"]
df["speedup"] = (df["ndvi_calc_time"][0] / df["containers"][0]) / (df["ndvi_calc_time"] / df["containers"])

print(df.to_string())

# Speedup
df.plot.scatter(x="containers", y="speedup")
plt.ylim([0, round(max(df["speedup"])+1)])
z = np.polyfit(df["containers"], df["speedup"], 4)
p = np.poly1d(z)
plt.plot(df["containers"], p(df["containers"]))
plt.show()

# Speed up with read/write
df.plot.scatter(x="containers", y="speedup_RW")
plt.ylim([0, round(max(df["speedup_RW"])+1)])
z = np.polyfit(df["containers"], df["speedup_RW"], 4)
p = np.poly1d(z)
plt.plot(df["containers"], p(df["containers"]))
plt.show()

# Total average image processing time
df.plot.scatter(x="containers", y="total_image_proc_time")
plt.ylim([0, round(max(df["total_image_proc_time"])+1)])
z = np.polyfit(df["containers"], df["total_image_proc_time"], 4)
p = np.poly1d(z)
plt.plot(df["containers"], p(df["containers"]))
plt.show()

# Average NDVI calculation time per image
df.plot.scatter(x="containers", y="ndvi_calc_time")
plt.ylim([0, round(max(df["ndvi_calc_time"])+1)])
z = np.polyfit(df["containers"], df["ndvi_calc_time"], 4)
p = np.poly1d(z)
plt.plot(df["containers"], p(df["containers"]))
plt.show()

# Read time
df.plot.scatter(x="containers", y="read_time")
plt.ylim([0, round(max(df["read_time"])+1)])
z = np.polyfit(df["containers"], df["read_time"], 1)
p = np.poly1d(z)
plt.plot(df["containers"], p(df["containers"]))
plt.show()

# Write time
df.plot.scatter(x="containers", y="write_time")
plt.ylim([0, round(max(df["write_time"])+1)])
z = np.polyfit(df["containers"], df["write_time"], 1)
p = np.poly1d(z)
plt.plot(df["containers"], p(df["containers"]))
plt.show()

