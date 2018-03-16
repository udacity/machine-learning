import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.insert(0, '../lib')
from visuals import Visuals


# retrive data of 'Q36', 'Q38','Q40'c
df = pd.read_csv("../2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")

#columns to sum to make a new feature called Q43TOTAL
sitting_hours_columns = ['Q43A','Q43B','Q43C','Q43D','Q43E','Q43F','Q43G1','Q43G2','Q43G3']

#replacing values which indicate "Refused" or "Don't know"
values_to_replace = [98,99]
for sitting_hours_column in sitting_hours_columns:
    for value_to_replace in values_to_replace:
        df[sitting_hours_column].replace(value_to_replace,df[sitting_hours_column].mean(),True)

columun = 'Q43TOTAL'
df[columun] = df[sitting_hours_columns].sum(axis=1)

def make_histogram(num_of_classes,r_min,r_max, title):
        # Classificating continuous values to appropriate range.
        vs = Visuals()
        ranges, sum_of_each_range =  vs.count_each_num_of_values_belongs_to_each_class(df[columun], num_of_classes,r_min,r_max,'tuples')

        # Making labels
        labels = list(ranges)

        # Setting the positions and width for the bars
        pos = range(len(sum_of_each_range))
        width = 0.25

        # Plotting  bars
        fig, ax = plt.subplots(figsize=(10,5))

        # Configuration of the bars
        rects = plt.bar(
                pos,
                sum_of_each_range,
                width,
                alpha=0.5,
                color='#4169E1',
                label=labels
        )

        # Setting magins above each bar
        ax.margins(y=0.2)

        # Setting the x axis label
        ax.set_xlabel('Minutes')

        # Set the y axis label
        ax.set_ylabel('Numer of Samples')

        # Setting the chart's title

        ax.set_title(title)

        # Setting the position of the x ticks
        ax.set_xticks(pos)

        # Setting the labels for the x ticks
        ax.set_xticklabels(labels)

        # Displays the number of samples above each bar
        vs.autolabel(ax, rects)

        # Adding grid to the plot
        plt.grid()

        # Showing the plot
        plt.show()

# To make histograms, I have to count nums of values which belong to each_range.
# This is a setting for it.
# Output Example: OrderedDict([('0-200', 948), ('201-400', 31), ('401-600', 17)])
r_min = 0 # set a lower limit of range
r_max = 4000 # set a higher limit of range
num_of_classes = 8 # The number of classes
title = 'Q43TOTAL: Total minutes per day the respondents spent for sitting during certain activities in the past 7days'
make_histogram(num_of_classes,r_min,r_max,title)

# Making a histogram which focuses on the range where a lot of respondents belongs to
r_min = 0 # set a lower limit of range
r_max = 1200 # set a higher limit of range
num_of_classes = 12
title = title + '\n (Only shows the range between 0 to 1200)'

# Showing the histogram
make_histogram(num_of_classes,r_min,r_max,title)

