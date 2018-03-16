import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.insert(0, '../lib')
from visuals import Visuals


# Loading the dataset
df = pd.read_csv("../2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")
column_name = 'Q43F'

# Removing unnecessary lines which contain unnecessary values
vs = Visuals()
df = df[np.logical_not(df[column_name].isin([98,99]))]

# Displaying min and max values of the column
vs.display_min_and_max_values(df,column_name,column_name + ' min-max : ', ' to ')


def make_histogram(num_of_classes, r_min, r_max):
    # Getting counts of each range
    vs = Visuals()
    ranges, sum_of_each_range = vs.count_each_num_of_values_belongs_to_each_class(df[column_name], num_of_classes, r_min, r_max, 'tuples')

    # Making labels
    labels = list(ranges)

    # Setting positions and width for the bars
    pos = range(len(sum_of_each_range))
    width = 0.50

    # Plotting bars
    fig, ax = plt.subplots(figsize=(10, 5))

    # Configuration of the bars
    rects = plt.bar(
        pos,
        sum_of_each_range,
        width,
        alpha=0.5,
        color='#4169E1',
        label=labels
    )
    # Setting margins above each bar
    ax.margins(y=0.2)

    # Setting x axis label
    ax.set_xlabel('Minutes')

    # Setting y axis label
    ax.set_ylabel('Numer of Samples')

    # Setting chart's title
    ax.set_title('Q43F: Minutes the respondents spent for sitting activities during doing hobbies per day in the past 7 days')

    # Setting position of the x ticks
    ax.set_xticks(pos)

    # Setting labels for the x ticks
    ax.set_xticklabels(labels)

    # Displays a number of samples above each bar
    vs.autolabel(ax,rects)

    # Adding grid to the plot
    plt.grid()

    # Showing the plot
    plt.show()


# To make histograms, I have to count nums of values which belong to each_range
# This is a setting for it.
# Output Example: OrderedDict([('0-200', 948), ('201-400', 31), ('401-600', 17)])
r_min = 0 # set a lower limit of range
r_max = 1400 # set a higher limit of range
num_of_classes = 7 # The number of classes

# Making and showing a histogram
make_histogram(num_of_classes,r_min,r_max)