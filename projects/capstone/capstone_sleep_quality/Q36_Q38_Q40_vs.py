import pandas as pd
import matplotlib.pyplot as plt
from visuals import Visuals
import sys

# retrive data of 'Q36', 'Q38','Q40'
df = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")

columns = 'Q36', 'Q38','Q40'

# print each min and max value
vs = Visuals()
for column in columns:
    vs.display_min_and_max_values(df,column,column + ' min-max : ', ' to ')

# Function which makes a histogram with multiple columns.
# I have to make same kind of histogram two times, so I made an easy function
def make_histogram(num_of_classes,r_min,r_max,title):
        # Classificating continuous values to appropriate range.
        vs = Visuals()
        Q36_classes, Q36_values =  vs.classificate(df['Q36'], num_of_classes,r_min,r_max,'tuples')
        Q38_classes, Q38_values =  vs.classificate(df['Q38'], num_of_classes,r_min,r_max,'tuples')
        Q40_classes, Q40_values =  vs.classificate(df['Q40'], num_of_classes,r_min,r_max,'tuples')

        # Setting labels
        labels = Q36_classes

        # Setting width for the bars and the positions
        width = 0.50
        step = int(width * 4)
        pos = range(1,len(Q36_values) * step,step)

        # Plotting the bars
        fig, ax = plt.subplots(figsize=(10,5))

        # Creating each bar
        rects1 = plt.bar(
                pos,
                Q36_values,
                width,
                alpha=0.5,
                color='#EE3224',
                label=labels
        )

        rects2 = plt.bar(
                [p + width for p in pos],
                Q38_values,
                width,
                alpha=0.5,
                color='#F78F1E',
                label=labels
        )

        rects3 = plt.bar(
                [p + (width * 2) for p in pos],
                Q40_values,
                width,
                alpha=0.5,
                color='#FFC222',
                label=labels
        )

        # Setting the x axis label
        ax.set_xlabel('Minutes')

        # Setting the y axis label
        ax.set_ylabel('Number of Samples')

        # Setting the chart's title
        ax.set_title(title)

        # Setting the position of the x ticks
        ax.set_xticks([p + width for p in pos])

        # Setting the labels for the x ticks
        ax.set_xticklabels(labels)

        # Making a legend.
        plt.legend(['Q36 : Vigorous Exercise', 'Q38 : Moderate Exercise', 'Q40 : Light Exercise'], loc='upper right')

        # Adding grid to the plot
        plt.grid()

        #Showing the plot
        plt.show()




# To make histograms, I have to classificate continuous values to appropriate range in 'make_histogram' function.
# This is a setting for it.
r_min = 0 # set a lower limit of range
r_max = 1600 # set a higher limit of range
num_of_classes = 8 # The number of classes
title = 'Minutes respondents spent for each type of exercise per day in the past 7 days.'

#Make and show histogram 1
make_histogram(num_of_classes,r_min,r_max,title)

#Setting for histogram 2
r_min = 0 # set a lower limit of range
r_max = 240 # set a higher limit of range
num_of_classes = 8 # The number of classes
title = 'Minutes respondents spent for each type of exercise per day in the past 7 days.\n(Only shows the range between 0 to 240 min)'

#Make and show histogram 2
make_histogram(num_of_classes,r_min,r_max,title)
