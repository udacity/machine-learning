import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('../lib')
from visuals import Visuals

# retrive d
df = pd.read_csv("../2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")
columns = ['Q36', 'Q38','Q40']

# print each min and max value
vs = Visuals()
for column in columns:
    vs.display_min_and_max_values(df,column,column + ' min-max : ', ' to ')

# Function which makes a histogram with multiple columns.
def make_histogram(num_of_classes,r_min,r_max,title):
        # Getting counts of each range
        vs = Visuals()
        Q36_classes, Q36_values =  vs.count_each_num_of_values_belongs_to_each_class(df['Q36'], num_of_classes,r_min,r_max,'tuples')
        Q38_classes, Q38_values =  vs.count_each_num_of_values_belongs_to_each_class(df['Q38'], num_of_classes,r_min,r_max,'tuples')
        Q40_classes, Q40_values =  vs.count_each_num_of_values_belongs_to_each_class(df['Q40'], num_of_classes,r_min,r_max,'tuples')

        # Setting labels
        labels = Q36_classes

        # Setting width for the bars
        width = 0.50

        # Setting position of the bars
        step = int(width * 4)
        pos = range(1,len(Q36_values) * step,step)

        # Plotting bars
        fig, ax = plt.subplots(figsize=(10,5))

        # Configurations of the bars
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

        # Setting margin above each bar
        ax.margins(y=0.2)

        # Setting a x axis label
        ax.set_xlabel('Minutes')

        # Setting a y axis label
        ax.set_ylabel('Number of Samples')

        # Setting a chart's title
        ax.set_title(title)

        # Setting position of the x ticks
        ax.set_xticks([p + width for p in pos])

        # Setting  labels for the x ticks
        ax.set_xticklabels(labels)

        # Displays a number of samples above each bar
        fontsize = 8.5
        vs.autolabel(ax, rects1, fontsize)
        vs.autolabel(ax, rects2, fontsize)
        vs.autolabel(ax, rects3, fontsize)

        # Making a legend.
        plt.legend(['Q36 : Vigorous Physical Activities', 'Q38 : Moderate Physical Activities', 'Q40 : Light Physical Activities'], loc='upper right')

        # Adding grid to the plot
        plt.grid()

        # Showing the plot
        plt.show()




# Setting for histogram 1
# This is a setting for it.
r_min = 0 # set a lower limit of range
r_max = 1600 # set a higher limit of range
num_of_classes = 8 # The number of classes
title = 'Minutes the respondents spent for each intensity of physical activities per day in the past 7 days.'

# Make and show histogram 1
make_histogram(num_of_classes,r_min,r_max,title)

# Setting for histogram 2
r_min = 0 # set a lower limit of range
r_max = 240 # set a higher limit of range
num_of_classes = 8 # The number of classes
title = title + '\n(Only shows the range between 0 to 240 min)'

# Make and show histogram 2
make_histogram(num_of_classes,r_min,r_max,title)
