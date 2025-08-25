# -*- coding: utf-8 -*-
"""
Created on 2025/8/4 14:08

@author: starry
"""

import geopandas as gpd
import matplotlib.pyplot as plt
from libpysal.weights import Queen
from esda.moran import Moran_Local
from esda.getisord import G_Local

# 1. Read the Shapefile
gdf = gpd.read_file("/Users/starry/Documents/GIS/Applied Project(Academic)/Picture1/Transport Disadvantage.shp")

# 2. Projection conversion
gdf = gdf.to_crs(epsg=27700)

# 3. Delete the missing values
gdf = gdf[gdf["IMD_NormIM"].notna()].copy()

# 4. Set the analysis variables
y = gdf["IMD_NormIM"]

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

from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


custom_colors = ["#1f77b4", "#d62728", "#8c564b", "#7f7f7f"]  # 蓝、灰、棕、红


labels = ["Low-Low","Low-High", "High-Low", "High-High"]
patches = [mpatches.Patch(color=clr, label=lbl) for clr, lbl in zip(custom_colors, labels)]


fig, ax = plt.subplots(1, 1, figsize=(10, 8))
gdf.plot(
    column="moran_cluster",
    categorical=True,
    cmap=ListedColormap(custom_colors),
    legend=False,
    ax=ax
)
plt.title("Local Moran's I Cluster Map (IMD)", fontsize=14)
plt.axis("off")


plt.legend(handles=patches, loc='lower left', title="Cluster Type")
plt.show()

# 9. Getis-Ord Gi*
import matplotlib as mpl

fig, ax = plt.subplots(1, 1, figsize=(10, 8))
gdf.plot(column="GiZ", cmap="RdBu", ax=ax, vmin=-3, vmax=3)

# add colorbar（
sm = plt.cm.ScalarMappable(cmap="RdBu", norm=plt.Normalize(vmin=-3, vmax=3))
sm._A = []
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Gi* Z-score')
cbar.set_ticks([-3, -1.5, 0, 1.5, 3])
cbar.set_ticklabels(['High Deprivation', '', 'Mean', '', 'Low Deprivation'])

plt.title("Getis-Ord Gi* Z-Score Map (IMD)", fontsize=14)
plt.axis("off")
plt.show()


gdf.to_file("IMD_hotspot_result.shp")