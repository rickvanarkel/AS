# importing packages
import pandas as pd
import seaborn as sns
import geopandas as gpd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx

# reading datafiles
link_bridges = './_uncleaned_data/Bridges_simplesheet.csv'
link_BMMS = './_uncleaned_data/BMMS_overview.xlsx'
link_roads = './_uncleaned_data/Roads_InfoAboutEachLRP.csv'
link_roads2 = './_uncleaned_data/_roads.tcv'

# creating pd dataframes
df_bridges = pd.read_csv(link_bridges, sep=';')
df_BMMS = pd.read_excel(link_BMMS)
df_roads = pd.read_csv(link_roads)
df_roads2 = pd.read_csv(link_roads2, sep='\t', low_memory=False, skiprows=[0], header=None)

#print(df_roads2.head(5))
print(df_bridges.head(5))

# creating gpd files
shape_bangladesh_link = './shapefiles/Bangladesh.shp'
shapefile_bangladesh = gpd.read_file(shape_bangladesh_link)
shapefile_bangladesh = shapefile_bangladesh.to_crs(epsg=3857)# (epsg=3106)

shape_bangladesh_link2 = './shapefiles/BGD_adm0.shp'
shapefile_bangladesh2 = gpd.read_file(shape_bangladesh_link2)
shapefile_bangladesh2 = shapefile_bangladesh2.to_crs(epsg=3857)# (epsg=3106)

# run the subfiles


# under this, collect cleaned dataframes from other files

# under this, write the datafiles to original format and export for zip?
