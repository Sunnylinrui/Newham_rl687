# -*- coding: utf-8 -*-
"""
Created on 2025/8/4 15:56

@author: starry
"""

import geopandas as gpd
import matplotlib.pyplot as plt
from libpysal.weights import Queen
from esda.moran import Moran_Local
from esda.getisord import G_Local

# 1. Read the Shapefile
gdf = gpd.read_file("/Users/starry/Documents/GIS/Applied Project(Academic)/Picture1/Bus_5min_Accessibility.shp")

# 2. Projection conversion
gdf = gdf.to_crs(epsg=27700)

# 3. Delete the missing values
gdf = gdf[gdf["5min_Bus_N"].notna()].copy()

# 4. Set the analysis variables
y = gdf["5min_Bus_N"]

# 5. Build the Queen adjacency matrix
w = Queen.from_dataframe(gdf)
w.transform = 'r'  # row-standardized

# 6. Local Moran's I
m_local = Moran_Local(y, w)
gdf["moran_I"] = m_local.Is
gdf["moran_p"] = m_local.p_sim
gdf["moran_cluster"] = m_local.q  # 1=HH, 2=LH, 3=LL, 4=HL

# 7. Getis-Ord Gi*
gi = G_Local(y, w)
gdf["GiZ"] = gi.Zs
gdf["Gi_p"] = gi.p_sim

# 8. Local Moran’s I
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
gdf.plot(column="moran_cluster", categorical=True, cmap="Set1", legend=True, ax=ax)
plt.title("Local Moran's I Cluster Map (5min Bus Accessibility)", fontsize=14)
plt.axis("off")
plt.show()

# 9. Getis-Ord Gi*
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
gdf.plot(column="GiZ", cmap="RdBu_r", legend=True, ax=ax, vmin=-3, vmax=3)
plt.title("Getis-Ord Gi* Z-Score Map (5min Bus Accessibility)", fontsize=14)
plt.axis("off")
plt.show()


gdf.to_file("5minBus_hotspot_result.shp")