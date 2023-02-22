import main as AS
import pandas as pd
import seaborn as sns
import geopandas as gpd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import contextily as cx

# AS.df_bridges is the dataset where...
# AS.df_BMMS is the dataset where...

print(AS.df_bridges.head(5))
#print(AS.df_BMMS.head(5))

# A map with all the shapefile of Bangladesh
fig, ax = plt.subplots(figsize=(8,8))

AS.shapefile_bangladesh.plot(ax=ax, edgecolor='white', linewidth=0.3)

cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
ax.set_axis_off()
ax.set_title('The country of Bangladesh')

plt.show()
