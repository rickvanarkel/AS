import numpy
import main as AS
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

clean_df = pd.DataFrame({'lon' : [], 'lat' : []})

for df in rdict.values():
    df['lon_dif'] = abs(df['lon'].astype(float).diff())
    df['lat_dif'] = abs(df['lat'].astype(float).diff())
    df.loc[df['lon_dif'] > 0.01, 'lon'] = numpy.NAN
    df.loc[df['lat_dif'] > 0.01, 'lat'] = numpy.NAN
    df = df.interpolate()
    clean_df = clean_df.append(df)
print(clean_df)

AS.df_roads.insert(5, 'gap', '')
AS.df_roads[['lon', 'lat']] = clean_df[['lon', 'lat']]
AS.df_roads.to_csv('_roads_cleaned.csv', index=False)

sns.set(color_codes=True)
sns.scatterplot(data = rdict['N1']['lon'])
plt.show()
#

# fouten die naast elkaar liggen of begin of eindpunt zijn kunnen niet gefixt worden via deze methode

# overige pogingen om data fixen:

# print(AS.df_roads['lon'].describe())
# print(AS.df_roads['lat'].describe())

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


# def find_outliers(col):
#
#     q1 = col.quantile(.25)
#     q3 = col.quantile(.75)
#     IQR = q3 - q1
#     ll = q1 - (1.5*IQR)
#     ul = q3 + (1.5*IQR)
#     upper_outliers = col[col > ul].index.tolist()
#     lower_outliers = col[col < ll].index.tolist()
#     bad_indices = list(set(upper_outliers + lower_outliers))
#     return(bad_indices)
# #
# def outlier_treatment(datacolumn):
#     sorted(datacolumn)
#     Q1,Q3 = np.percentile(datacolumn , [25,75])
#     IQR = Q3 - Q1
#     lower_range = Q1 - (1.5 * IQR)
#     upper_range = Q3 + (1.5 * IQR)
#     return lower_range, upper_range


# for df in rdict.values():
#     bad_indexes = []
#     for col in df.columns:
#         #print(df[col])
#         lowerbound,upperbound = outlier_treatment(df[col])
#         outliers = df[(df[col] < lowerbound) | (df[col] > upperbound)]
#         print(f' These are the {outliers}')
    #print(df)