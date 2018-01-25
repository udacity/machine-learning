import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from visuals import Visuals
import sys


# retrive data of 'Q36', 'Q38','Q40'c
df = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")

#columns to sum to make a new feature called Q43TOTAL
sitting_hours_columns = ['Q43A','Q43B','Q43C','Q43D','Q43E','Q43F','Q43G1','Q43G2','Q43G3']

#replacing values which indicate "Refused" or "Don't know"
values_to_replace = [98,99]
for sitting_hours_column in sitting_hours_columns:
    for value_to_replace in values_to_replace:
        df[sitting_hours_column].replace(value_to_replace,df[sitting_hours_column].mean(),True)

columun = 'Q43TOTAL'
df[columun] = df[sitting_hours_columns].sum(axis=1)

def make_histogram(num_of_classes,r_min,r_max):
        # Classificating continuous values to appropriate range.
        vs = Visuals()
        ranges, sum_of_each_range =  vs.classificate(df[columun], num_of_classes,r_min,r_max,'tuples')

        # Making labels
        labels = list(ranges)

        # Setting the positions and width for the bars
        pos = range(len(sum_of_each_range))
        width = 0.25

        # Plotting the bars
        fig, ax = plt.subplots(figsize=(10,5))

        # Create a bars
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

        # Set the y axis label
        ax.set_ylabel('Numer of Samples')

        # Setting the chart's title

        ax.set_title('Q43TOTAL: total time per day respondents spend sitting during some activities in the past 7days')

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
r_max = 4000 # set a higher limit of range
num_of_classes = 8 # The number of classes
make_histogram(num_of_classes,r_min,r_max)

# Making a histogram which focuses on the range where a lot of respondents belongs to
r_min = 0 # set a lower limit of range
r_max = 1200 # set a higher limit of range
num_of_classes = 12
# Showing the histogram
make_histogram(num_of_classes,r_min,r_max)

