import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from visuals import Visuals
import sys


# retrive data of 'Q36', 'Q38','Q40'c
df = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")
columun = 'q29a'

df = df[np.logical_not(df[columun].isin([97,98,99]))]
print df['q29a'].min()
print df['q29a'].max()
# sys.exit()
# print df

def make_histogram(num_of_classes,r_min,r_max,title):
        # Classificating continuous values to appropriate range.
        vs = Visuals()
        ranges, sum_of_each_range =  vs.classificate(df[columun], num_of_classes,r_min,r_max,'tuples')

        # Making labels
        labels = list(ranges)

        # Setting the positions and width for the bars
        pos = range(len(sum_of_each_range))
        width = 0.5

        # Plotting the bars
        fig, ax = plt.subplots(figsize=(10,5))

        # Create a bars
        plt.bar(
                pos,
                sum_of_each_range,
                width,
                alpha=0.5,
                color='#7C5852',
                label=labels
        )

        # Setting the x axis label
        ax.set_xlabel('Numer of Servings')

        # Set the y axis label
        ax.set_ylabel('Numer of Samples')

        # Setting the chart's title
        ax.set_title(title)

        # Setting the position of the x ticks
        ax.set_xticks(pos)

        # Setting the labels for the x ticks
        ax.set_xticklabels(labels)

        # Adding grid to the plot
        plt.grid()

        # Adjusting shape of plot
        plt.subplots_adjust(top=0.85)

        # Showing the plot
        plt.show()

# To make histograms, I have to classificate continuous values to appropriate range.
# This is a setting for it.
# Output Example: OrderedDict([('0-200', 948), ('201-400', 31), ('401-600', 17)])
r_min = 0 # set a lower limit of range
r_max = 64 # set a higher limit of range
num_of_classes = 8 # The number of classes
title = 'q29a: Number of 12 ounce servings of caffeinated beverages \n respondents take between 5:00 AM and noon on an average weekday or workday'
make_histogram(num_of_classes,r_min,r_max,title)

# Making a histogram which focuses on the range where a lot of respondents belongs to
r_min = 0 # set a lower limit of range
r_max = 10 # set a higher limit of range
num_of_classes = 11
title =  title + '\n (Only shows the range between 0 to 10 servings)'
#
# # Showing the histogram
make_histogram(num_of_classes,r_min,r_max,title)

