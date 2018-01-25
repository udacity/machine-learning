import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import sys
import pandas as pd

#Getting the dataset
all_data = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")



#Defining Y Labels
y_labels = [
        '12:00 AM (Midnight)',
        '12:01 AM to 12:59 AM',
        '1:00 AM to 1:59 AM',
        '2:00 AM to 5:00 AM',
        '5:01 AM to 8:59 AM',
        '9:00 AM to 11:59 AM',
        '12:00 PM (Noon) to 6:59 PM',
        '7:00 PM to 7:59 PM',
        '8:00 PM to 8:59 PM',
        '9:00 PM to 9:14 PM',
        '9:15 PM to 9:29 PM',
        '9:30 PM to 9:44 PM',
        '9:45 PM to 9:59 PM',
        '10:00 PM to 10:14 PM',
        '10:15 PM to 10:29 PM',
        '10:30 PM to 10:44 PM',
        '10:45 PM to 10:59 PM',
        '11:00 PM to 11:14 PM',
        '11:15 PM to 11:29 PM',
        '11:30 PM to 11:44 PM',
        '11:45 PM to 11:59 PM',
        'Refused',
        'Don\'t know',
    ]






# Applying one hot encoding and making it easy to calculate sum of each category.
dummies_q1 = pd.get_dummies(all_data['q1'])
dummies_q3 = pd.get_dummies(all_data['q3'])

# In q3, there's no samples and there's no column for '7',
# so I manually added it
dummies_q3[7] = 0
dummies_q3 = dummies_q3.sort_index(axis=1)

plt_title_q1 = 'Time the respondents get into bed in a weekday'
plt_title_q3 =  'Time the respondents get into bed in a weekend'

def make_horizontal_histogram(dummies,plt_title):
    # The matplotlib.rcdefaults() command will restore the standard matplotlib default settings.
    plt.rcdefaults()

    # Getting  matplotlib.figure.Figure object and Axes object or array of Axes objects.
    fig, ax = plt.subplots(1, figsize=(10, 5))

    # Setting colors of bar to make easy to distinguish bars of night time and daytime.
    noon_bars = [4, 5, 6]
    not_answered_bars = [21, 22]
    colors = []
    noon_color = '#ffd732'
    night_color = '#5c3cab'
    not_answered_color = '#CCCCCC'
    for index, y_label in enumerate(y_labels):
        if index in noon_bars:
            colors.append(noon_color)
        elif index in not_answered_bars:
            colors.append(not_answered_color)
        else:
            colors.append(night_color)

    # Getting sum of each category
    def get_sum_of_each_category(dummies):
        sum_of_each_category_dict = {}
        for index, row in dummies.iterrows():
            for index_2, value in row.iteritems():
                if index_2 not in sum_of_each_category_dict:
                    sum_of_each_category_dict[index_2] = 0
                if value == 1:
                    sum_of_each_category_dict[index_2] += 1
        sum_of_each_category = np.array(list(sum_of_each_category_dict.values()))
        return sum_of_each_category

    sum_of_each_category = get_sum_of_each_category(dummies)

    # Setting y coordinates of the bars
    y_pos = np.arange(len(y_labels))

    # Making a horizontal bar plot
    ax.barh(y_pos, sum_of_each_category, align='center', color=colors, alpha=0.8)
    ax.set_yticks(y_pos)  # it specifies y values
    ax.set_yticklabels(y_labels)  # specify people y tick labels
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Number of each answer')  # lbel for x axis
    ax.set_title(plt_title)  # specifies title

    # Making a legend
    noon_patch = mpatches.Patch(color=noon_color, label='Day Time')
    night_patch = mpatches.Patch(color=night_color, label='Night Time')
    not_answered_patch = mpatches.Patch(color=not_answered_color, label='Not Answered')
    plt.legend(handles=[night_patch, noon_patch, not_answered_patch])

    # Adjusting shape of plot
    plt.subplots_adjust(left=0.25, right=0.8)

    #Showing a plot
    plt.show()


make_horizontal_histogram(dummies_q1,plt_title_q1)
make_horizontal_histogram(dummies_q3,plt_title_q3)