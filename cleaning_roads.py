import main as AS
import pandas as pd
import seaborn as sns
import geopandas as gpd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import contextily as cx
import warnings
warnings.filterwarnings('ignore')
#
# print(AS.df_roads)
# print(AS.df_roads2)

# A map with all the shapefile of Bangladesh
# fig, ax = plt.subplots(figsize=(8,8))
#
# AS.shapefile_bangladesh.plot(ax=ax, edgecolor='white', linewidth=0.3)
#
# cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
# ax.set_axis_off()
# ax.set_title('The country of Bangladesh')
#
# plt.show()

roadnames = (AS.df_roads['road'].append(AS.df_roads['road'])).unique()
rdict = {}

for x in roadnames:
    df = AS.df_roads.loc[AS.df_roads['road'] == x, ['lon', 'lat']]  # maakt df van elke weg apart met lat
    rdict[x] = df

sns.set(color_codes=True)
sns.scatterplot(data = rdict['N1']['lon'])
plt.show()

print(rdict['N1'])
z =  rdict['N1']['lon']

print(AS.df_roads['lon'].describe())
print(AS.df_roads['lat'].describe())