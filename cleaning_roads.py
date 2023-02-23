import numpy

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

roadnames = (AS.df_roads['road'].append(AS.df_roads['road'])).unique()
rdict = {}

for x in roadnames:
    df = AS.df_roads.loc[AS.df_roads['road'] == x, ['lon', 'lat']]  # maakt df van elke weg apart met lat
    rdict[x] = df

sns.set(color_codes=True)
sns.scatterplot(data = rdict['N1']['lon'])
plt.show()

print(AS.df_roads['lon'].describe())
print(AS.df_roads['lat'].describe())

# for key in rdict:
#     print(key)
#     outliers = []
#     threshold = 1.8
#     mean = np.mean(rdict[key]['lat'])
#     std = np.std(rdict[key]['lat'])
#     print(mean)
#     print(std)
#
#     for value in rdict[key]['lat']:
#         #print(value)
#         z_score = (value - mean)/std
#         if np.abs(z_score) > threshold:
#             outliers.append(value)

for df in rdict.values():
    df['lon_dif'] = abs(df['lon'].astype(float).diff())
    df['lat_dif'] = abs(df['lat'].astype(float).diff())
    df.loc[df['lon_dif'] > 0.01, 'lon'] = numpy.NAN
    df.loc[df['lat_dif'] > 0.01, 'lat'] = numpy.NAN

    #print(df)