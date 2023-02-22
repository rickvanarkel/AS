import main as AS
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
#print(AS.df_roads.head(5))
#print(AS.df_roads2.head(5))
#AS.df_roads2.to_excel('Rooadstcv.xlsx')

print(AS.df_roads['lat'].describe())
sns.set(color_codes=True)
sns.scatterplot(data = AS.df_roads, x=AS.df_roads.index, y='lat')
plt.show()


roadnames = (AS.df_roads['road'].append(AS.df_roads['road'])).unique()

#print(roadnames)

road_dict = {}
# for x in roadnames:
#     print(x)

# for data_dict in d.values():
#    x = data_dict.keys()
#    y = data_dict.values()
#    plt.scatter(x,y,color=colors.pop())

# plt.legend(d.keys())
# plt.show()

for x in roadnames:
    df = AS.df_roads.loc[AS.df_roads['road'] == x, 'lat']  # maakt df van elke weg apart met lat

    print(df.describe())


