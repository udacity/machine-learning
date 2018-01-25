import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from visuals import Visuals
import sys



# Retriving data of 'Q36', 'Q38','Q40'
df = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")
column_name = 'Q43F'

vs = Visuals()
df = df[np.logical_not(df[column_name].isin([98,99]))]
vs.display_min_and_max_values(df,column_name,column_name + ' min-max : ', ' to ')
# sys.exit()

def make_histogram(num_of_classes, r_min, r_max):
    # Classificating continuous values to appropriate range.
    vs = Visuals()
    ranges, sum_of_each_range = vs.classificate(df[column_name], num_of_classes, r_min, r_max, 'tuples')

    #Making labels
    labels = list(ranges)

    # Setting the positions and width for the bars
    pos = range(len(sum_of_each_range))
    width = 0.50

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(10, 5))

    # Creating a bar
    plt.bar(
        pos,
        sum_of_each_range,
        width,
        alpha=0.5,
        color='#4169E1',
        label=labels
    )
    # Setting the x axis label
    ax.set_xlabel('Minutes')

    # Setting the y axis label
    ax.set_ylabel('Numer of Samples')

    # Setting the chart's title
    ax.set_title('Q43F: Minutes respondents spent for sitting activities during doing hobbies per day in the past 7 days')

    # Setting the position of the x ticks
    ax.set_xticks(pos)

    # Setting the labels for the x ticks
    ax.set_xticklabels(labels)

    # Adding grid to the plot
    plt.grid()

    # Showing the plot
    plt.show()


# To make histograms, I have to classificate continuous values to appropriate range.
# This is a setting for it.
# Output Example: OrderedDict([('0-200', 948), ('201-400', 31), ('401-600', 17)])
r_min = 0 # set a lower limit of range
r_max = 1400 # set a higher limit of range
num_of_classes = 7 # The number of classes

# Making and showing histogram 1
make_histogram(num_of_classes,r_min,r_max)

# # Making a histogram which focuses on the range where a lot of respondents belongs to
# r_min = 0 # set a lower limit of range
# r_max = 16 # set a higher limit of range
# num_of_classes = 17 # The number of classes

# # Showing the histogram
# make_histogram(num_of_classes,r_min,r_max)
