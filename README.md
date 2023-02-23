# EPA1352 Lab Assignment 1: Data Quality

Group 9

- Rick van Arkel ~ 4974859
- Laura Drost ~ 5066034
- Inge Faber ~ 4457617
- Daan de Jager ~ 4702972
- Susan Ruinaard ~ 4650441

Last updated: 24-02-2023

## Project description

## Model usage

### Cleaning Roads
The code provided appears to be an attempt to clean a dataset containing data about roads in Bangladesh. The code reads in the original dataset from the file main.py, which presumably contains errors that need to be fixed.

The first step in the code is to create a dictionary called rdict that maps each unique road name in the dataset to a Pandas DataFrame containing the longitude and latitude coordinates of each point along that road. This is achieved by looping over the unique road names in the dataset, creating a new DataFrame for each road that contains only the longitude and latitude columns, and adding that DataFrame to the dictionary under the corresponding road name.

The code then goes on to use the Seaborn library to create a scatter plot of the longitude coordinates for one of the roads in the dataset (N1), presumably to visualize any errors in the data. However, since the scatter plot is only showing the longitude coordinates, it is not clear how useful this visualization would be in identifying errors related to latitude coordinates.

The next step in the code is to create an empty Pandas DataFrame called empty_df to hold the cleaned data. The code then loops over each DataFrame in the rdict dictionary and performs the following operations:

1. Calculate the absolute difference between consecutive longitude and latitude values using the diff() method.
2. Set any longitude or latitude values where the absolute difference is greater than 0.01 to NaN.
3. Interpolate missing values using the interpolate() method.

The resulting DataFrame with cleaned data is then appended to empty_df. Finally, the cleaned longitude and latitude values in empty_df are used to replace the corresponding values in the original dataset, which is then written to a new file called _clean_roads.csv.

Overall, this code appears to be a reasonable approach for cleaning a dataset containing errors related to longitude and latitude coordinates. However, without more context about the specific errors in the dataset, it is difficult to say whether this approach will be effective in identifying and correcting all of the errors. Additionally, the code could be improved by incorporating error-handling and data validation checks to ensure that the cleaned data is valid and accurate.





## Used data


## Installations needed

### Dependencies 
The following libraries have to be installed to run the model:

- Pandas
- Seaborn 
- Geopandas
- Numpy
- Matplotlib
- Matplotlib.pyplot 
- Networkx

## Acknowledgements
