# importing packages
import pandas as pd
import seaborn as sns
import geopandas as gpd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx

# reading datafiles
link_bridges = './_uncleaned_data/Bridges.xlsx'
link_BMMS = './_uncleaned_data/BMMS_overview.xlsx'
link_roads = './_uncleaned_data/Roads_InfoAboutEachLRP.csv'
link_roads2 = './_uncleaned_data/_roads.tcv'

# creating pd dataframes
df_bridges = pd.read_excel(link_bridges)
df_BMMS = pd.read_excel(link_BMMS)
df_roads = pd.read_csv(link_roads)
df_roads2 = pd.read_csv(link_roads2, sep='\t', low_memory=False, skiprows=[0], header=None)


print(df_roads2.head(5))


# run the subfiles


# under this, collect cleaned dataframes from other files

# under this, write the datafiles to original format and export for zip?
