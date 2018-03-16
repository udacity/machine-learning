import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.insert(0, '../lib')
from visuals import Visuals


# Loading the dataset
df = pd.read_csv("../2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")

# Creating labels
labels = [
    'Q43A:\nWatching\n television',
    'Q43B:\nUsing\n a computer',
    'Q43C:\nReading',
    'Q43D:\nSocializing with\n friends or\n family',
    'Q43E:\nTraveling in\n motor vehicle\n or on\n public transport',
    'Q43F:\nDoing\n hobbies',
    'Q43G1-G3:\nSomething\n else'
]

sitting_hours_columns_1 = ['Q43A','Q43B','Q43C','Q43D','Q43E','Q43F']
sitting_hours_columns_2 = ['Q43G1','Q43G2','Q43G3']  # Q43G1-G3

# Calculating mean of each category
def get_mean_of_each_classes(columns):
    mean_of_each_class = []
    for column in columns:
        mean_of_each_class.append(df[column].mean())
    return mean_of_each_class

# Getting means of the columns
mean_of_each_class_1 =  get_mean_of_each_classes(sitting_hours_columns_1)
mean_of_each_class_2 =  get_mean_of_each_classes(sitting_hours_columns_2)

# Adding mean_of_each_class_2 to mean_of_each_class_1
mean_of_each_class_1.append(np.mean(mean_of_each_class_2))

# Setting positions and width for the bars
pos = range(len(mean_of_each_class_1))
width = 0.25

# Plotting bars
fig, ax = plt.subplots(figsize=(10, 5))

# Configuration of the bars
rects = plt.bar(
    pos,
    mean_of_each_class_1,
    width,
    1,
    alpha=0.5,
    color='#4169E1',
    label=labels
)

# Setting margins above each bar
ax.margins(y=0.2)

# Setting a x axis label
ax.set_xlabel('Activities while sitting.')

# Set a y axis label
ax.set_ylabel('Minutes')

# Setting a chart's title
ax.set_title('Average minutes per day the respondents spent for each activity while sitting in the past 7days.')

# Setting position of the x ticks
ax.set_xticks(pos)

# Setting labels for the x ticks
ax.set_xticklabels(labels)

# Displays a number of samples above each bar
vs = Visuals()
vs.autolabel(ax, rects)

# Adding grid to the plot
plt.grid()

# Showing the plot
plt.show()

