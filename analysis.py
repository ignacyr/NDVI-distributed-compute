import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("measurements.csv")[20:]
df = df.loc[df["ram_limit"] == 1.5]
df = df.groupby("containers", as_index=False).mean()
df = df.sort_values(by="containers")
df["acceleration"] = df["total_time"][0] / df["total_time"]

print(df.to_string())

df.plot(x="containers", y="acceleration")
plt.show()

df.plot(x="containers", y="total_image_proc_time")
plt.show()

df.plot(x="containers", y="ndvi_calc_time")
plt.show()

df.plot(x="containers", y="read_time")
plt.show()

df.plot(x="containers", y="write_time")
plt.show()

