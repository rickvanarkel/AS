# importing packages
import pandas as pd
import seaborn as sns
import geopandas as gpd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx

# reading datafiles
link_bridges = './Bridges.xlsx'
link_BMMS = './BMMS_overview.xlsx'
link_roads = './Roads_InfoAboutEachLRP.csv'

# creating pd dataframes
df_bridges = pd.read_excel(link_bridges)
df_BMMS = pd.read_excel(link_BMMS)
df_roads = pd.read_csv(link_roads)

# under this, collect cleaned dataframes from other files

# under this, write the datafiles to original format and export for zip?
