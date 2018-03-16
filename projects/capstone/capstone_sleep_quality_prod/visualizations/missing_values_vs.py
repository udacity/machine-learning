import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../lib')
sys.path.append("../")
import pre_process
import columns_config

# Loading the dataset
df = pd.read_csv("../2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")

# Dropping target values and storing to another variable.
features = df.drop('q30', axis = 1)
sleep_quality = df['q30']

# Setting new features
df['Q43TOTAL'] = 0
df['Q36Q38Q40TOTAL'] = 0
df['Q3Q1DIF'] = 0
df['Q4Q2DIF'] = 0
df['Q4Q2DIFQ3Q1DIFTOTAL'] = 0


# Making a preprocess object
pre_process_obj = pre_process.PreProcess(df,columns_config.columns_config)
pre_process_obj.extract_data()

# Sorting skews in descending order
nums_of_missing_values = pre_process_obj.df.isnull().sum()
nums_of_missing_values.sort_values(ascending=False, inplace=True)

# Selecting columns which has missing_values more than 500
reduced_nums_of_missing_values = nums_of_missing_values.loc[nums_of_missing_values > 500]


def make_horizontal_histogram(y_labels,values):
    # The matplotlib.rcdefaults() command restores the standard matplotlib default settings.
    plt.rcdefaults()

    # Getting  matplotlib.figure.Figure object and Axes object or array of Axes objects.
    fig, ax = plt.subplots(1)

    # Setting width of bars
    width = 0.8


    # Setting y coordinates of the bars
    y_pos = np.arange(len(y_labels))

    # Making a horizontal bar plot
    ax.barh(y_pos, values, align='center',height = width, color='gray', alpha=0.8)
    ax.set_yticks(y_pos)  # Specifying y ticks
    ax.set_yticklabels(y_labels)  # Specifying labels of y ticks
    ax.invert_yaxis()  # Sorting the columns in decending order
    ax.set_ylabel('Features')  # labels for y axis
    ax.set_xlabel('Number of missing values')  # labels for x axis
    ax.set_title('Number of missing values in each feature')  # Specifying title of the plot


    # Adjusting shape of the plot
    plt.subplots_adjust(left=0.25, right=0.8)

    # Adding grid to the plot
    plt.grid()

    # Showing the plot
    plt.show()


# Getting labels and values to make a horizontal histogram
labels = reduced_nums_of_missing_values.keys()
values = reduced_nums_of_missing_values.values

# Making a horizontal histogram
make_horizontal_histogram(labels,values)
