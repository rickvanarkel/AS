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
import cartopy.crs as ccrs

link_in_country = './_uncleaned_data/bridges from GIS/bridges_in_bangladesh.csv'
link_close_road = './_uncleaned_data/bridges from GIS/bridges_near_osmroads.csv'
link_lrpinfo = './_uncleaned_data/Roads_InfoAboutEachLRP.csv'

# creating pd dataframes
df_bridges_in_country = pd.read_csv(link_in_country)
df_bridges_near_roads = pd.read_csv(link_close_road)
df_lrp_info = pd.read_csv(link_lrpinfo)

# AS.df_bridges is the dataset where...
# AS.df_BMMS is the dataset where...

#print(AS.df_bridges.head(5))
#print(AS.df_BMMS.head(5))

'''
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
gdf_bridges_lonlat = gpd.GeoDataFrame(df_bridges_lonlat_coord) # crs="EPSG:3857"

#gdf_bridges_lonlat.crs = AS.shapefile_bangladesh.crs
#gdf_bridges_lonlat = gdf_bridges_lonlat.to_crs(epsg=3857)

#gdf_bridges_lonlat.to_csv('./lonlat_bridges_test.csv')

print(df_bridges_lonlat_coord.dtypes)

print(df_bridges_lonlat_coord)

'''

# Check for missing values
print(AS.df_BMMS.isnull().sum())
print(AS.df_bridges.isnull().sum())

BMMS_lonlat = ['road','LRPName', 'lat', 'lon']
df_BMMS_lonlat = AS.df_BMMS.loc[:, BMMS_lonlat]

# Check if coordinates are swapped, they are not
print(df_BMMS_lonlat.sort_values('lat', ascending=False).head(5))

AS.df_BMMS['bridge_id'] = AS.df_BMMS['road'] + AS.df_BMMS['LRPName']

df_BMMS_definitive = AS.df_BMMS



# Add columns to df if the bridge is close to a road, and within Bangladesh
'''
# creating pd dataframes
df_bridges_in_country 
df_bridges_near_roads 
AS.df_BMMS
df_BMMS_lonlat

Het liefst kolommen toevoegen aan df_BMMS_lonlat, twee kolommen: eentje met 'outside country' en de andere met 'far from road'
Werken met true/false of een verschillende string als het niet in een van de dataframes staat
'''
'''
df_BMMS_lonlat['outside country'] = True
print(df_bridges_in_country.head(5))
for x in df_bridges_in_country['lrp']:
    if x in df_BMMS_lonlat['LRPName']:
        print('hoi')
        df_BMMS_lonlat.loc[x, 'outside country'] = False
'''

print(df_BMMS_lonlat.nunique())

print(df_BMMS_lonlat.isnull().sum())

df_BMMS_lonlat['bridge_id'] = df_BMMS_lonlat['road'] + df_BMMS_lonlat['LRPName']
df_bridges_near_roads['bridge_id']= df_bridges_near_roads['road'] + df_bridges_in_country['LRPName']
df_bridges_in_country['bridge_id'] = df_bridges_in_country['road'] + df_bridges_in_country['LRPName']

'''
# Merge df_BMMS_lonlat and df_bridges_in_country on 'LRPName' and 'road'
merged = pd.merge(df_BMMS_lonlat, df_bridges_in_country, on=['LRPName', 'road'], how='left')

# Set 'outside country' to False for matching rows
merged.loc[merged['bridge_id'].notnull(), 'outside country'] = False

# Update df_BMMS_lonlat with the merged data
df_BMMS_lonlat.update(merged[['lon', 'lat', 'outside country']])
'''

df_BMMS_lonlat['outside country'] = True
for x in df_bridges_in_country['bridge_id']:
    if df_BMMS_lonlat['bridge_id'].isin([x]).any():
        df_BMMS_lonlat.loc[(df_BMMS_lonlat['bridge_id'] == x), 'outside country'] = False

print(f'Number of points outside of the country: {df_BMMS_lonlat["outside country"].value_counts()[True]}')


df_BMMS_lonlat['far from road'] = True
for x in df_bridges_near_roads['bridge_id']:
    if df_BMMS_lonlat['bridge_id'].isin([x]).any():
        df_BMMS_lonlat.loc[df_BMMS_lonlat['bridge_id'] == x, 'far from road'] = False

print(f'Number of points far from road: {df_BMMS_lonlat["far from road"].value_counts()[True]}')

df_BMMS_lonlat.loc[df_BMMS_lonlat['outside country'], ['lon', 'lat']] = np.nan
df_BMMS_lonlat.loc[df_BMMS_lonlat['far from road'], ['lon', 'lat']] = np.nan

print(df_BMMS_lonlat.isnull().sum())

df_lrp_info['road_id'] = df_lrp_info['road'] + df_lrp_info['lrp']

# Create a boolean mask for rows with missing lat and lon values
mask = df_BMMS_lonlat['lat'].isnull() & df_BMMS_lonlat['lon'].isnull()

counter = 0
wrongbridgeid = []

for x in df_lrp_info['road_id']:
    if df_BMMS_lonlat['bridge_id'].isin([x]).any():
        counter += 1
    else:
        wrongbridgeid.append(x)



print(df_lrp_info['road_id'].nunique())
print(df_BMMS_lonlat['bridge_id'].nunique())

print(counter)


# Loop over the road IDs in df_lrp_info
for x in df_lrp_info['road_id']:
    # Check if x matches any bridge IDs in df_BMMS_lonlat
    if df_BMMS_lonlat['bridge_id'].isin([x]).any():
        # Get the lat and lon values from df_lrp_info for this road ID
        lat, lon = df_lrp_info.loc[df_lrp_info['road_id'] == x, ['lat', 'lon']].values[0]

        # Update the lat and lon values in df_BMMS_lonlat where the mask is True
        df_BMMS_lonlat.loc[mask & (df_BMMS_lonlat['bridge_id'] == x), ['lat', 'lon']] = [lat, lon]

print(df_BMMS_lonlat.isnull().sum())

print(df_BMMS_definitive.head(5))





'''
for x in df_lrp_info['road_id']:
    for df_BMMS_lonlat['lat', 'lon'].isnull():
        if df_BMMS_lonlat['bridge_id'].isin([x]).any():
            df_BMMS_lonlat.loc[df_BMMS_lonlat['bridge_id'] == x, 'lat', 'lon'] = df_lrp_info['lat', 'lon']
            #df_BMMS_lonlat.loc[df_BMMS_lonlat['bridge_id'] == x, 'lon'] = df_lrp_info['lon']
'''


'''
#gdf_bridges_lonlat.crs = AS.shapefile_bangladesh.crs
#gdf_bridges_lonlat = gdf_bridges_lonlat.to_crs(epsg=3857)
#gdf_bridges_lonlat.to_csv('./lonlat_bridges_test.csv')
#print(df_bridges_lonlat_coord.dtypes)
#print(df_bridges_lonlat_coord)
#print(df_bridges_plotcoord)
#df_bridges_lonlat['LatitudeDegree'] = df_bridges_lonlat[]
#print(df_bridges_lonlat)
'''
'''
# Prepare for plotting
df_BMMS_lonlat_coord['geometry'] = [Point (xy) for xy in zip(df_BMMS_lonlat_coord['lon'], df_BMMS_lonlat_coord['lat'])]
gdf_BMMS_lonlat = gpd.GeoDataFrame(df_BMMS_lonlat_coord, crs="EPSG:3857") # crs="EPSG:3857"

# A map with all the shapefile of Bangladesh
#fig, ax = plt.subplots(figsize=(8,8))

fig, ax = plt.subplots(subplot_kw={'projection': crs})

AS.shapefile_bangladesh.plot(ax=ax, edgecolor='white', linewidth=0.3)
gdf_BMMS_lonlat.plot(ax=ax, cmap='Reds')

#cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
#ax.set_axis_off()
#ax.set_title('The country of Bangladesh')
#plt.show()
'''

