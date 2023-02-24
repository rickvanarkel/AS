import numpy
import main as AS
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Get unique road names and initialize dictionary
roadnames = (AS.df_roads['road'].append(AS.df_roads['road'])).unique()
rdict = {}

# Loop over road names and create DataFrame for each road containing longitude and latitude coordinates
for x in roadnames:
    df = AS.df_roads.loc[AS.df_roads['road'] == x, ['lon', 'lat']]
    rdict[x] = df

# Plot scatter plot of longitude coordinates for road 'N1'
sns.set(color_codes=True)
sns.scatterplot(data = rdict['N1']['lon'])
plt.show()

# Create a new, empty DataFrame called 'clean_df'
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
    clean_df = clean_df.append(df)

print(clean_df)

# Insert a new column called 'gap' into the 'AS.df_roads' DataFrame
AS.df_roads.insert(5, 'gap', '')
# Replace 'lon' and 'lat' columns in 'AS.df_roads' with cleaned values from 'clean_df'
AS.df_roads[['lon', 'lat']] = clean_df[['lon', 'lat']]
# Write cleaned DataFrame to CSV file called '_roads_cleaned.csv'
AS.df_roads.to_csv('_roads_cleaned.csv', index=False)

# Plot scatter plot of longitude coordinates for road 'N1' with cleaned values
sns.scatterplot(data = rdict['N1']['lon'])
plt.show()

### Other attempts for cleaning the data:

# print(AS.df_roads['lon'].describe())
# print(AS.df_roads['lat'].describe())

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
#             # if the absolute value of the z-score is greater than the threshold, the current value is considered an outlier
#             outliers.append(value)
#             # add the current value to the list of outliers
#
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
#     # loop over each value in the rdict dictionary (which should be a DataFrame)
#     bad_indexes = []
#     for col in df.columns:
#         # loop over each column in the DataFrame
#         lowerbound,upperbound = outlier_treatment(df[col])
#         # calculate the lower and upper bounds for outlier detection
#         outliers = df[(df[col] < lowerbound) | (df[col] > upperbound)]
#         # find the rows that contain outliers for the current column
#         print(f' These are the {outliers}')
#     print(df)
