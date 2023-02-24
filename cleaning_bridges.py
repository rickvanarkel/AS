import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point

link_bridges = './_uncleaned_data/Bridges_simplesheet.csv'
link_BMMS = './_uncleaned_data/BMMS_overview.xlsx'

# Obtained from GIS preprocessing
link_in_country = './_uncleaned_data/bridges from GIS/bridges_in_bangladesh.csv'
link_close_road = './_uncleaned_data/bridges from GIS/bridges_near_osmroads.csv'

# Cleaned lrp info
link_lrpinfo = './_roads3.csv'
#link_lrpinfo = './Roads_InfoAboutEachLRP.csv'

# creating pd dataframes
df_bridges = pd.read_csv(link_bridges, sep=';')
df_BMMS = pd.read_excel(link_BMMS)
df_bridges_in_country = pd.read_csv(link_in_country)
df_bridges_near_roads = pd.read_csv(link_close_road)
df_lrp_info = pd.read_csv(link_lrpinfo)

# Check for missing values
print(df_BMMS.isnull().sum())
print(df_bridges.isnull().sum())

# Creating a dataframe with the essential information
BMMS_lonlat = ['road','LRPName', 'lat', 'lon']
df_BMMS_lonlat = df_BMMS.loc[:, BMMS_lonlat]

# Check if coordinates are swapped, they are not (eventually not needed)
print(df_BMMS_lonlat.sort_values('lat', ascending=False).head(5))

# Create bridge id
df_BMMS['bridge_id'] = df_BMMS['road'] + df_BMMS['LRPName']

# Some checks
print(df_BMMS_lonlat.nunique())
print(df_BMMS_lonlat.isnull().sum())

# Making bridge and road id's
df_BMMS_lonlat['bridge_id'] = df_BMMS_lonlat['road'] + df_BMMS_lonlat['LRPName']
df_bridges_near_roads['bridge_id']= df_bridges_near_roads['road'] + df_bridges_in_country['LRPName']
df_bridges_in_country['bridge_id'] = df_bridges_in_country['road'] + df_bridges_in_country['LRPName']
df_lrp_info['road_id'] = df_lrp_info['road'] + df_lrp_info['lrp']

# Adding information about the criteria to the dataframes
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

# Set lon and lat to NaN if the criteria is false
df_BMMS_lonlat.loc[df_BMMS_lonlat['outside country'], ['lon', 'lat']] = np.nan
df_BMMS_lonlat.loc[df_BMMS_lonlat['far from road'], ['lon', 'lat']] = np.nan

# Dataframe for visualisation
df_BMMS_lonlat_nan = df_BMMS_lonlat

# A check on the missing values
print(df_BMMS_lonlat.isnull().sum())

# Collecting wrong bridge id's
wrongbridgeid = []
for x in df_lrp_info['road_id']:
    if df_BMMS_lonlat['bridge_id'].isin([x]).any():
        pass
    else:
        wrongbridgeid.append(x)

print(df_lrp_info['road_id'].nunique())
print(df_BMMS_lonlat['bridge_id'].nunique())

# Create a boolean mask for rows with missing lat and lon values
mask = df_BMMS_lonlat['lat'].isnull() & df_BMMS_lonlat['lon'].isnull()

# Loop over the road IDs in df_lrp_info
for x in df_lrp_info['road_id']:
    # Check if x matches any bridge IDs in df_BMMS_lonlat
    if df_BMMS_lonlat['bridge_id'].isin([x]).any():
        # Get the lat and lon values from df_lrp_info for this road ID
        lat, lon = df_lrp_info.loc[df_lrp_info['road_id'] == x, ['lat', 'lon']].values[0]

        # Update the lat and lon values in df_BMMS_lonlat where the mask is True
        df_BMMS_lonlat.loc[mask & (df_BMMS_lonlat['bridge_id'] == x), ['lat', 'lon']] = [lat, lon]

print(df_BMMS_lonlat.isnull().sum())

# Prepare for plotting
df_BMMS_plotting = df_BMMS
df_BMMS_plotting['geometry'] = [Point (xy) for xy in zip(df_BMMS_plotting['lon'], df_BMMS_plotting['lat'])]
gdf_BMMS_plotting = gpd.GeoDataFrame(df_BMMS_plotting, crs="EPSG:3857") # crs="EPSG:3857"

df_BMMS_lonlat['geometry'] = [Point (xy) for xy in zip(df_BMMS_lonlat['lon'], df_BMMS_lonlat['lat'])]
gdf_BMMS_lonlat = gpd.GeoDataFrame(df_BMMS_lonlat, crs="EPSG:3857") # crs="EPSG:3857"

df_BMMS_lonlat_nan['geometry'] = [Point (xy) for xy in zip(df_BMMS_lonlat_nan['lon'], df_BMMS_lonlat_nan['lat'])]
gdf_BMMS_lonlat_nan = gpd.GeoDataFrame(df_BMMS_lonlat_nan, crs="EPSG:3857") # crs="EPSG:3857"

# Plots for examining the lon and lat
fig, ax = plt.subplots(figsize=(8,8))

#gdf_BMMS_plotting.plot(ax=ax, cmap='Reds') # old coordinates
gdf_BMMS_lonlat.plot(ax=ax, cmap='Blues') # new coordinates
#gdf_BMMS_lonlat_nan.plot(ax=ax, cmap='Greens') # before new coordinates

plt.show()

# Updating the original dataframe
df_BMMS_definitive = df_BMMS
print(df_BMMS_definitive.head(5))

# Exporting the dataframe to the original data type
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point

link_bridges = './_uncleaned_data/Bridges_simplesheet.csv'
link_BMMS = './_uncleaned_data/BMMS_overview.xlsx'

# Obtained from GIS preprocessing
link_in_country = './_uncleaned_data/bridges from GIS/bridges_in_bangladesh.csv'
link_close_road = './_uncleaned_data/bridges from GIS/bridges_near_osmroads.csv'

# Cleaned lrp info
link_lrpinfo = './_uncleaned_data/Roads_InfoAboutEachLRP.csv'

# creating pd dataframes
df_bridges = pd.read_csv(link_bridges, sep=';')
df_BMMS = pd.read_excel(link_BMMS)
df_bridges_in_country = pd.read_csv(link_in_country)
df_bridges_near_roads = pd.read_csv(link_close_road)
df_lrp_info = pd.read_csv(link_lrpinfo)

# Check for missing values
print(df_BMMS.isnull().sum())
print(df_bridges.isnull().sum())

# Creating a dataframe with the essential information
BMMS_lonlat = ['road','LRPName', 'lat', 'lon']
df_BMMS_lonlat = df_BMMS.loc[:, BMMS_lonlat]

# Check if coordinates are swapped, they are not (eventually not needed)
print(df_BMMS_lonlat.sort_values('lat', ascending=False).head(5))

# Create bridge id
df_BMMS['bridge_id'] = df_BMMS['road'] + df_BMMS['LRPName']

# Some checks
print(df_BMMS_lonlat.nunique())
print(df_BMMS_lonlat.isnull().sum())

# Making bridge and road id's
df_BMMS_lonlat['bridge_id'] = df_BMMS_lonlat['road'] + df_BMMS_lonlat['LRPName']
df_bridges_near_roads['bridge_id']= df_bridges_near_roads['road'] + df_bridges_in_country['LRPName']
df_bridges_in_country['bridge_id'] = df_bridges_in_country['road'] + df_bridges_in_country['LRPName']
df_lrp_info['road_id'] = df_lrp_info['road'] + df_lrp_info['lrp']

# Adding information about the criteria to the dataframes
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

# Set lon and lat to NaN if the criteria is false
df_BMMS_lonlat.loc[df_BMMS_lonlat['outside country'], ['lon', 'lat']] = np.nan
df_BMMS_lonlat.loc[df_BMMS_lonlat['far from road'], ['lon', 'lat']] = np.nan

# Dataframe for visualisation
df_BMMS_lonlat_nan = df_BMMS_lonlat

# A check on the missing values
print(df_BMMS_lonlat.isnull().sum())

# Collecting wrong bridge id's
wrongbridgeid = []
for x in df_lrp_info['road_id']:
    if df_BMMS_lonlat['bridge_id'].isin([x]).any():
        pass
    else:
        wrongbridgeid.append(x)

print(df_lrp_info['road_id'].nunique())
print(df_BMMS_lonlat['bridge_id'].nunique())

# Create a boolean mask for rows with missing lat and lon values
mask = df_BMMS_lonlat['lat'].isnull() & df_BMMS_lonlat['lon'].isnull()

# Loop over the road IDs in df_lrp_info
for x in df_lrp_info['road_id']:
    # Check if x matches any bridge IDs in df_BMMS_lonlat
    if df_BMMS_lonlat['bridge_id'].isin([x]).any():
        # Get the lat and lon values from df_lrp_info for this road ID
        lat, lon = df_lrp_info.loc[df_lrp_info['road_id'] == x, ['lat', 'lon']].values[0]

        # Update the lat and lon values in df_BMMS_lonlat where the mask is True
        df_BMMS_lonlat.loc[mask & (df_BMMS_lonlat['bridge_id'] == x), ['lat', 'lon']] = [lat, lon]

print(df_BMMS_lonlat.isnull().sum())

# Prepare for plotting
df_BMMS_plotting = df_BMMS
df_BMMS_plotting['geometry'] = [Point (xy) for xy in zip(df_BMMS_plotting['lon'], df_BMMS_plotting['lat'])]
gdf_BMMS_plotting = gpd.GeoDataFrame(df_BMMS_plotting, crs="EPSG:3857") # crs="EPSG:3857"

df_BMMS_lonlat['geometry'] = [Point (xy) for xy in zip(df_BMMS_lonlat['lon'], df_BMMS_lonlat['lat'])]
gdf_BMMS_lonlat = gpd.GeoDataFrame(df_BMMS_lonlat, crs="EPSG:3857") # crs="EPSG:3857"

df_BMMS_lonlat_nan['geometry'] = [Point (xy) for xy in zip(df_BMMS_lonlat_nan['lon'], df_BMMS_lonlat_nan['lat'])]
gdf_BMMS_lonlat_nan = gpd.GeoDataFrame(df_BMMS_lonlat_nan, crs="EPSG:3857") # crs="EPSG:3857"

# Plots for examining the lon and lat
fig, ax = plt.subplots(figsize=(8,8))
#gdf_BMMS_plotting.plot(ax=ax, cmap='Reds') # old coordinates
gdf_BMMS_lonlat.plot(ax=ax, cmap='Blues') # new coordinates
#gdf_BMMS_lonlat_nan.plot(ax=ax, cmap='Greens') # before new coordinates
plt.show()

# Updating the original dataframe
print(df_BMMS.columns.values.tolist())
print(df_BMMS_lonlat.columns.values.tolist())

print(df_BMMS.shape)
print(df_BMMS_lonlat.shape)

# A quick method to merge the two files. Merge and dropping columns was also possible
# The indexing stayed the same since we did not change order, and the shapes are the same
df_BMMS_definitive = df_BMMS
df_BMMS_definitive['lat'] = df_BMMS_lonlat['lat']
df_BMMS_definitive['lon'] = df_BMMS_lonlat['lon']

print(df_BMMS_definitive.head(5))

# Exporting the dataframe to the original data type
df_BMMS_definitive.to_excel('BMMS_overview.xlsx', index=False)

# Some trial and error under this!
'''
# Our try to do the GIS analyses with Geopandas, but the projection of the points did not work (points on the figure vs geopoints on the map)

#gdf_bridges_lonlat.crs = shapefile_bangladesh.crs
#gdf_bridges_lonlat = gdf_bridges_lonlat.to_crs(epsg=3857)
#gdf_bridges_lonlat.to_csv('./lonlat_bridges_test.csv')
#df_bridges_lonlat['LatitudeDegree'] = df_bridges_lonlat[]

# Prepare for plotting
df_BMMS_lonlat_coord['geometry'] = [Point (xy) for xy in zip(df_BMMS_lonlat_coord['lon'], df_BMMS_lonlat_coord['lat'])]
gdf_BMMS_lonlat = gpd.GeoDataFrame(df_BMMS_lonlat_coord, crs="EPSG:3857") # crs="EPSG:3857"

# A map with all the shapefile of Bangladesh
#fig, ax = plt.subplots(figsize=(8,8))

shapefile_bangladesh.plot(ax=ax, edgecolor='white', linewidth=0.3)
gdf_BMMS_lonlat.plot(ax=ax, cmap='Reds')

#cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
#ax.set_axis_off()
#ax.set_title('The country of Bangladesh')
#plt.show()
'''

'''
# Our try to work with the Bridges file

bridges_lonlat = ['Number', 'LatitudeDegree', 'LatitudeMinute', 'LatitudeSecond', 'LongitudeDegree', 'LongitudeMinute', 'LongitudeSecond']
df_bridges_lonlat = df_bridges.loc[:, bridges_lonlat]

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

#gdf_bridges_lonlat.crs = shapefile_bangladesh.crs
#gdf_bridges_lonlat = gdf_bridges_lonlat.to_crs(epsg=3857)

#gdf_bridges_lonlat.to_csv('./lonlat_bridges_test.csv')

print(df_bridges_lonlat_coord.dtypes)

print(df_bridges_lonlat_coord)
'''
