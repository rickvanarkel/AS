import numpy
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

link_bridges = './_uncleaned_data/Bridges_simplesheet.csv'
link_BMMS = './_uncleaned_data/BMMS_overview.xlsx'
link_roads = './_uncleaned_data/Roads_InfoAboutEachLRP.csv'
link_roads2 = './_uncleaned_data/_roads.tcv'

# creating pd dataframes
df_bridges = pd.read_csv(link_bridges, sep=';')
df_BMMS = pd.read_excel(link_BMMS)
df_roads = pd.read_csv(link_roads)
df_roads2 = pd.read_csv(link_roads2, sep='\t', low_memory=False, skiprows=[0], header=None)

# Get unique road names and initialize dictionary
roadnames = (df_roads['road'].append(df_roads['road'])).unique()
rdict = {}

# Loop over road names and create DataFrame for each road containing longitude and latitude coordinates
for x in roadnames:
    df = df_roads.loc[df_roads['road'] == x, ['lon', 'lat']]
    rdict[x] = df

print(df_roads['lon'].describe())
print(df_roads['lat'].describe())

# Plot scatter plot of longitude coordinates for road 'N1' to visualize outliers
# To show scatter plots of other roads, for longitude or latitude, change [N1]['lon']
sns.set(color_codes=True)
sns.scatterplot(data = rdict['N1']['lon'])
plt.title("Original longitude value per LRP for road N1")
plt.show()

# Create a new, empty DataFrame called 'clean_df' with columns named 'lat' and 'lon'
clean_df = pd.DataFrame({'lon' : [], 'lat' : []})

# Loop over DataFrames in 'rdict' and interpolate missing longitude and latitude values
for df in rdict.values():
    # Calculate difference between each longitude and latitude value
    df['lon_dif'] = abs(df['lon'].astype(float).diff())
    df['lat_dif'] = abs(df['lat'].astype(float).diff())
    # Replace values greater than 0.01 with NaN
    df.loc[df['lon_dif'] > 0.01, 'lon'] = numpy.NAN
    df.loc[df['lat_dif'] > 0.01, 'lat'] = numpy.NAN
    # Interpolate all NaN values
    df = df.interpolate()
    # Add cleaned data to the new dataframe
    clean_df = clean_df.append(df)

print(clean_df)

# Insert a new column called 'gap' into the 'df_roads' DataFrame (otherwise JAVA will nog visualize the roads)
df_roads.insert(5, 'gap', '')
# Replace 'lon' and 'lat' columns in 'df_roads' with cleaned values from 'clean_df'
df_roads[['lon', 'lat']] = clean_df[['lon', 'lat']]
# Write cleaned DataFrame to CSV file called '_roads_cleaned.csv'
df_roads.to_csv('_roads_cleaned.csv', index=False)

# Plot scatter plot of longitude coordinates for road 'N1' with cleaned values
# To show scatter plots of other roads, for longitude or latitude, change [N1]['lon']
sns.scatterplot(data = rdict['N1']['lon'])
plt.title("Cleaned longitude value per LRP for road N1")
plt.show()


### Other attempt for cleaning the data: ###


# print(df_roads['lon'].describe())
# print(df_roads['lat'].describe())

# for key in rdict:
#     # iterate over each key in the rdict dictionary
#     print(key)
#     # print the current key being processed
#     outliers = []
#     # initialize an empty list to hold the outliers
#     threshold = 1.8
#     # set the threshold for outlier detection
#     mean = np.mean(rdict[key]['lat'])
#     # calculate the mean of the 'lat' values for the current key
#     std = np.std(rdict[key]['lat'])
#     # calculate the standard deviation of the 'lat' values for the current key
#     print(mean)
#     print(std)
#
#
#     for value in rdict[key]['lat']:
#         # iterate over each value in the 'lat' list for the current key
#         #print(value)
#         z_score = (value - mean)/std
#         # calculate the z-score for the current value
#         if np.abs(z_score) > threshold:
#             # if the value of the z-score is greater than the threshold, the current value is considered an outlier
#             outliers.append(value)
#             # add the current value to the list of outliers
#
#


### Another attempt for cleaning the data: ###

# def find_outliers(col):
#     # define a function to find the outliers in a given column of data
#     q1 = col.quantile(.25)
#     # calculate the first quartile of the column
#     q3 = col.quantile(.75)
#     # calculate the third quartile of the column
#     IQR = q3 - q1
#     # calculate the interquartile range of the column
#     ll = q1 - (1.5*IQR)
#     # calculate the lower limit of the column
#     ul = q3 + (1.5*IQR)
#     # calculate the upper limit of the column
#     upper_outliers = col[col > ul].index.tolist()
#     # find the indices of values above the upper limit
#     lower_outliers = col[col < ll].index.tolist()
#     # find the indices of values below the lower limit
#     bad_indices = list(set(upper_outliers + lower_outliers))
#     # combine the two lists of outlier indices and remove duplicates
#     return(bad_indices)
#
# def outlier_treatment(datacolumn):
#     # define a function to perform outlier treatment on a given column of data
#     sorted(datacolumn)
#     # sort the values in the column (not sure if this is necessary)
#     Q1,Q3 = np.percentile(datacolumn , [25,75])
#     # calculate the first and third quartiles of the column
#     IQR = Q3 - Q1
#     # calculate the interquartile range of the column
#     lower_range = Q1 - (1.5 * IQR)
#     # calculate the lower limit of the column
#     upper_range = Q3 + (1.5 * IQR)
#     # calculate the upper limit of the column
#     return lower_range, upper_range
#
# for df in rdict.values():
#     # loop over each value in the rdict dictionary
#     bad_indexes = []
#     for col in df.columns:
#         # loop over each column in the DataFrame
#         lowerbound,upperbound = outlier_treatment(df[col])
#         # calculate the lower and upper bounds for outlier detection
#         outliers = df[(df[col] < lowerbound) | (df[col] > upperbound)]
#         # find the rows that contain outliers for the current column
#         print(f' These are the indexes of the outliers: {outliers}')
#     print(df)