import main as AS

import pandas as pd
import seaborn as sns
import geopandas as gpd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import contextily as cx

import main as AS
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import contextily as cx
import pandas as pd
warnings.filterwarnings('ignore')

print(AS.df_roads)
print(AS.df_roads2)

# A map with all the shapefile of Bangladesh
fig, ax = plt.subplots(figsize=(8,8))

AS.shapefile_bangladesh.plot(ax=ax, edgecolor='white', linewidth=0.3)

cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
ax.set_axis_off()
ax.set_title('The country of Bangladesh')

plt.show()

#print(AS.df_roads.head(5))
#print(AS.df_roads2.head(5))
#AS.df_roads2.to_excel('Rooadstcv.xlsx')

link_roads = './_uncleaned_data/Roads_InfoAboutEachLRP.csv'
link_roads2 = './_uncleaned_data/_roads.tcv'

df_roads = pd.read_csv(link_roads)
df_roads2 = pd.read_csv(link_roads2, sep='\t', low_memory=False, skiprows=[0], header=None)

print(AS.df_roads['lat'].describe())

sns.set(color_codes=True)
sns.scatterplot(data = AS.df_roads, x=AS.df_roads.index, y='lat')
plt.show()

roadnames = (AS.df_roads['road'].append(AS.df_roads['road'])).unique()

for data_dict in d.values():
   x = data_dict.keys()
   y = data_dict.values()
   plt.scatter(x,y,color=colors.pop())

plt.legend(d.keys())
plt.show()

rdict = {}

for x in roadnames:
    df = AS.df_roads.loc[AS.df_roads['road'] == x, 'lat']  # maakt df van elke weg apart met lat
    rdict[x].append(df)

print(rdict)
