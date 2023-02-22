import main as AS
import pandas as pd
import seaborn as sns
import geopandas as gpd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import contextily as cx
from shapely.geometry import Point, Polygon

# AS.df_bridges is the dataset where...
# AS.df_BMMS is the dataset where...

#print(AS.df_bridges.head(5))
#print(AS.df_BMMS.head(5))

bridges_lonlat = ['Number', 'LatitudeDegree', 'LatitudeMinute', 'LatitudeSecond', 'LongitudeDegree', 'LongitudeMinute', 'LongitudeSecond']
df_bridges_lonlat = AS.df_bridges.loc[:, bridges_lonlat]

# Check for missing values
# print(df_bridges_lonlat.isnull().sum())

# drop rows with NaN values, since this is another problem type. The rows with NaN values are saved in another df.
df_bridges_lonlat_coord = df_bridges_lonlat.dropna()
df_bridges_missingcoord = df_bridges_lonlat[df_bridges_lonlat.isnull().any(1)]

print(df_bridges_lonlat.shape)
print(df_bridges_missingcoord.shape)
print(df_bridges_lonlat_coord.shape)

# Fix the Seconds column to get rid of the comma
df_bridges_lonlat_coord.LatitudeSecond = df_bridges_lonlat_coord['LatitudeSecond'].str.replace(',','.').astype(float)
df_bridges_lonlat_coord.LongitudeSecond = df_bridges_lonlat_coord['LongitudeSecond'].str.replace(',','.').astype(float)

df_bridges_lonlat_coord.LatitudeSecond = df_bridges_lonlat_coord.LatitudeSecond.apply(lambda x: x*10).astype(int).astype(str)
df_bridges_lonlat_coord.LongitudeSecond = df_bridges_lonlat_coord.LongitudeSecond.apply(lambda x: x*10).astype(int).astype(str)

df_bridges_lonlat_coord.LatitudeDegree = df_bridges_lonlat_coord.LatitudeDegree.astype(int).astype(str)
df_bridges_lonlat_coord.LatitudeMinute = df_bridges_lonlat_coord.LatitudeMinute.astype(int).astype(str)
df_bridges_lonlat_coord.LongitudeDegree = df_bridges_lonlat_coord.LongitudeDegree.astype(int).astype(str)
df_bridges_lonlat_coord.LongitudeMinute = df_bridges_lonlat_coord.LongitudeMinute.astype(int).astype(str)

df_bridges_lonlat_coord['Latitude'] = df_bridges_lonlat_coord['LatitudeDegree'] + '.' + df_bridges_lonlat_coord['LatitudeMinute'] + df_bridges_lonlat_coord['LatitudeSecond']
df_bridges_lonlat_coord['Longitude'] = df_bridges_lonlat_coord['LongitudeDegree'] + '.' + df_bridges_lonlat_coord['LongitudeMinute'] + df_bridges_lonlat_coord['LongitudeSecond']

df_bridges_lonlat_coord['geometry'] = [Point (xy) for xy in zip(df_bridges_lonlat_coord['Longitude'], df_bridges_lonlat_coord['Latitude'])]
gdf_bridges_lonlat = gpd.GeoDataFrame(df_bridges_lonlat_coord, crs="EPSG:3857")

print(df_bridges_lonlat_coord.dtypes)

print(df_bridges_lonlat_coord)

#print(df_bridges_plotcoord)

#df_bridges_lonlat['LatitudeDegree'] = df_bridges_lonlat[]

#print(df_bridges_lonlat)

# A map with all the shapefile of Bangladesh
fig, ax = plt.subplots(figsize=(8,8))

AS.shapefile_bangladesh.plot(ax=ax, edgecolor='white', linewidth=0.3)
gdf_bridges_lonlat.plot(ax=ax)

cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
ax.set_axis_off()
ax.set_title('The country of Bangladesh')

plt.show()
