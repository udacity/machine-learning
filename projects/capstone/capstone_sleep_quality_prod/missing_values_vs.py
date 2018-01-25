import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from visuals import Visuals
import sys
import pre_process
import columns_config

# retrive data of 'Q36', 'Q38','Q40'c
df = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")
columun = 'q29c'

#Dropping target values and storing to another variable.
features = df.drop('q30', axis = 1)
sleep_quality = df['q30']

#Setting new features
df['Q43TOTAL'] = 0
df['Q36Q38Q40TOTAL'] = 0
df['Q3Q1DIF'] = 0
df['Q4Q2DIF'] = 0
df['Q4Q2DIFQ3Q1DIFTOTAL'] = 0


#Making a preprocess object
pre_process_obj = pre_process.PreProcess(df,columns_config.columns_config)
pre_process_obj.extract_data()

#Sorting skews in descending order
nums_of_missing_values = pre_process_obj.df.isnull().sum()
nums_of_missing_values.sort_values(ascending=False, inplace=True)



reduced_nums_of_missing_values = nums_of_missing_values.loc[nums_of_missing_values > 500]
#
# sys.exit()
# sys.exit()
def make_horizontal_histogram(y_labels,values):
    # The matplotlib.rcdefaults() command restores the standard matplotlib default settings.
    plt.rcdefaults()

    # Getting  matplotlib.figure.Figure object and Axes object or array of Axes objects.
    fig, ax = plt.subplots(1)

    height = 0.8


    # Setting y coordinates of the bars
    y_pos = np.arange(len(y_labels))

    # Making a horizontal bar plot
    ax.barh(y_pos, values, align='center',height = height, color='gray', alpha=0.8)
    ax.set_yticks(y_pos)  # it specifies y values
    ax.set_yticklabels(y_labels)  # specify people y tick labels
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Number of missing values')  # lbel for x axis
    ax.set_title('Number of missing values in each feature')  # specifies title


    # Adjusting shape of the plot
    plt.subplots_adjust(left=0.25, right=0.8)

    #Adding grid
    plt.grid()

    #Showing the plot
    plt.show()

#Showing a horizontal bar plot
# Showing the list of absolute skews

#Getting lables and values to make a horizontal histogram
labels = reduced_nums_of_missing_values.keys()
values = reduced_nums_of_missing_values.values

make_horizontal_histogram(labels,values)

# reduced_nums_of_missing_values = nums_of_missing_values[24:49]
# #Getting lables and values to make a horizontal histogram
# labels = reduced_nums_of_missing_values.keys()
# values = reduced_nums_of_missing_values.values
# make_horizontal_histogram(labels,values)
#
# reduced_nums_of_missing_values = nums_of_missing_values[49:74]
# #Getting lables and values to make a horizontal histogram
# labels = reduced_nums_of_missing_values.keys()
# values = reduced_nums_of_missing_values.values
# make_horizontal_histogram(labels,values)