import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("master/measurements.csv")
df = df.loc[df["ram_limit"] == 1.5]
df = df.sort_values(by="containers")
df["acceleration"] = 220 / df["total_time"]

print(df)

df.plot(x="containers", y="acceleration")
plt.show()

