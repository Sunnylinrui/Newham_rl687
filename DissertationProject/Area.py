# -*- coding: utf-8 -*-
"""
Created on 2025/8/23 01:04

@author: starry
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## 1. Data
data = {
    "Area": ["Stratford", "Canning Town", "Beckton", "East Ham"],
    "BusCAI": [0.72, 0.63, 0.54, 0.56],
    "RailCAI": [0.84, 0.56, 0.47, 0.22],
    "AverageCAI": [0.78, 0.60, 0.50, 0.39],
    "No Car": [66.6, 58.54, 41.4, 46.42],
    "White%": [39.83, 39.78, 45.36, 23.1],
}
df = pd.DataFrame(data)

#2. plotting
x = np.arange(len(df["Area"]))
width = 0.25

fig, ax1 = plt.subplots(figsize=(9,6))

# histogram
ax1.bar(x - width, df["BusCAI"], width, label="BusCAI")
ax1.bar(x, df["RailCAI"], width, label="RailCAI")
ax1.bar(x + width, df["AverageCAI"], width, label="AverageCAI")
ax1.set_ylabel("CAI (0–1)")
ax1.set_xticks(x)
ax1.set_xticklabels(df["Area"])
ax1.set_xlabel("Area")


#line chart（No Car & White%
ax2 = ax1.twinx()
ax2.plot(x, df["No Car"], marker="o", color="pink", label="No Car (%)")
ax2.plot(x, df["White%"], marker="s", color="red", label="White (%)")
ax2.set_ylabel("Percentage (%)")


lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="best")

plt.title("Public Transport Accessibility (CAI) + Socio-Demographic Indicators")
plt.tight_layout()
plt.show()