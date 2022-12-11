import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("master/measurements.csv")
df = df.loc[df["ram_limit"] == 1.5]
df = df.groupby("containers", as_index=False).mean()
df = df.sort_values(by="containers")
df["acceleration"] = df["total_time"][1] / df["total_time"]

print(df)

df.plot(x="containers", y="acceleration")
plt.show()

