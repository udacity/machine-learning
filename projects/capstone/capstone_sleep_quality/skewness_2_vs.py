import pandas as pd
import numpy as np
import pre_process
import columns_config
import sys
import scipy.stats as ss
import matplotlib.pyplot as plt
from colour import Color
# red = Color("red")
# colors = list(red.range_to(str(Color("yellow")),10))
# print colors


# for x in range(len(colors)):
#     print colors[x]
# sys.exit()
import matplotlib.patches as mpatches
all_data = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")
# print len(all_data.keys())
# print len(columns_config.columns_config.keys())
# sys.exit()
#Dropping target values and storing to another variable.
features = all_data.drop('q30', axis = 1)
sleep_quality = all_data['q30']


all_data['Q43TOTAL'] = 0
all_data['Q36Q38Q40TOTAL'] = 0
# all_data['Q4Q3Q2Q1DIF'] = 0
all_data['Q3Q1DIF'] = 0
all_data['Q4Q2DIF'] = 0
all_data['Q4Q2DIFQ3Q1DIFTOTAL'] = 0
#Making a preprocess object
pre_process_obj = pre_process.PreProcess(all_data,columns_config.columns_config)

#Making and Adding new features


pre_process_obj.convert_values()
pre_process_obj.convert_types()

#Making and Adding new features
sitting_hours_columns = ['Q43A','Q43B','Q43C','Q43D','Q43E','Q43F','Q43G1','Q43G2','Q43G3']
pre_process_obj.df['Q43TOTAL'] = pre_process_obj.df[sitting_hours_columns].sum(axis=1)
amount_of_exercise_columns= ['Q36','Q38','Q40']
pre_process_obj.df['Q36Q38Q40TOTAL'] = pre_process_obj.df[amount_of_exercise_columns].sum(axis=1)
pre_process_obj.df['Q3Q1DIF'] = pre_process_obj.df['Q3VALUE'] - pre_process_obj.df['Q1VALUE']
pre_process_obj.df['Q4Q2DIF'] = pre_process_obj.df['Q4VALUE'] - pre_process_obj.df['Q2VALUE']
pre_process_obj.df['Q4Q2DIFQ3Q1DIFTOTAL'] = pre_process_obj.df[['Q4Q2DIF','Q3Q1DIF']].sum(axis=1)


# pre_process_obj.raise_values_to_positive()
pre_process_obj.get_skews()


abs_skews = pre_process_obj.get_skews().abs()
abs_skews.sort_values(ascending=False, inplace=True)
labels = abs_skews.keys()

values = abs_skews.values
height = 0.8
# print len(labels)
# print len(values)
# sys.exit()
# print labels
# print values
# sys.exit()
# labels_1 = labels[:len(labels)/4]
# values_1 = values[:len(values)/4]
# labels_2 = labels[(len(labels)/4) :2 * (len(labels)/4)]
# values_2 = values[(len(values)/4) :2 * (len(labels)/4)]
# labels_3 = labels[2 * (len(labels)/4) :3 * (len(labels)/4)]
# values_3 = values[2 * (len(values)/4) :3 * (len(labels)/4)]
# labels_4 = labels[3 * (len(labels)/4) :(len(labels))]
# values_4 = values[3 * (len(values)/4) :(len(labels))]


def make_horizontal_histogram(y_labels,values):
    # The matplotlib.rcdefaults() command will restore the standard matplotlib default settings.
    plt.rcdefaults()

    # Getting  matplotlib.figure.Figure object and Axes object or array of Axes objects.
    # fig, ax = plt.subplots(1, figsize=(10, 5))
    fig, ax = plt.subplots(1)

    # Setting colors of bar to make easy to distinguish bars of night time and daytime.
    noon_bars = [4, 5, 6]
    not_answered_bars = [21, 22]
    # red = Color("#DD0001")
    # colors = list(red.range_to(Color("#D2BB00"), len(y_labels)))
    # colors_in_hex = []
    # for i in range(len(colors)):
    #     colors_in_hex.append(colors[i],10)
    colors_in_hex = [
        '#DD0001','#DD0503','#DD0A05','#DE0F08','#DE140A','#DE1A0D','#DF1F0F','#DF2412',
        '#E02914', '#E02F17', '#E03419', '#E1391B', '#E13E1E', '#E14420', '#E24923', '#E24E25',
        '#E35328', '#E3582A', '#E35E2D', '#E4632F', '#E46831', '#E56D34', '#E57336', '#E57839',
        '#E67D3B', '#E6823E', '#E68840', '#E78D43', '#E79245', '#E89747', '#E89D4A', '#E8A24C',
        '#E9A74F', '#E9AC51', '#EAB154', '#EAB756', '#EABC59', '#EBC15B', '#EBC65D', '#EBCC60',
        '#ECD162', '#ECD665', '#EDDB67', '#EDE16A', '#EDE66C', '#EEEB6F', '#EEF071', '#EFF674',
        # '#DD0001','#DD0503','#DD0A05','#DE0F08','#DE140A','#DE1A0D','#DF1F0F','#DF2412','#E02914','#E02F17','#E03419','#E1391B','#E13E1E','#E14420','#E24923',
        # '#E24E25','#E35328','#E3582A','#E35E2D','#E4632F','#E46831','#E56D34','#E57336','#E57839','#E67D3B','#E6823E','#E68840','#E78D43','#E79245','#E89747',
        # '#E89D4A','#E8A24C','#E9A74F','#E9AC51','#EAB154','#EAB756','#EABC59','#EBC15B','#EBC65D','#EBCC60','#ECD162','#ECD665','#EDDB67','#EDE16A','#EDE66C',
    ]
    # print len(colors_in_hex)
    # sys.exit()
    # colors = []
    # noon_color = '#ffd732'
    # night_color = '#5c3cab'
    # not_answered_color = '#CCCCCC'
    # for index, y_label in enumerate(y_labels):
    #     if index in noon_bars:
    #         colors.append(noon_color)
    #     elif index in not_answered_bars:
    #         colors.append(not_answered_color)
    #     else:
    #         colors.append(night_color)

    # # Getting sum of each category
    # def get_sum_of_each_category(dummies):
    #     sum_of_each_category_dict = {}
    #     for index, row in dummies.iterrows():
    #         for index_2, value in row.iteritems():
    #             if index_2 not in sum_of_each_category_dict:
    #                 sum_of_each_category_dict[index_2] = 0
    #             if value == 1:
    #                 sum_of_each_category_dict[index_2] += 1
    #     sum_of_each_category = np.array(list(sum_of_each_category_dict.values()))
    #     return sum_of_each_category
    #
    # sum_of_each_category = get_sum_of_each_category(dummies)

    # Setting y coordinates of the bars
    y_pos = np.arange(len(y_labels))
    # for range(len(y_labels))
    # Making a horizontal bar plot
    # width_list =  [width] * len(labels)
    ax.barh(y_pos, values, align='center',height = height, color=colors_in_hex, alpha=0.8)
    ax.set_yticks(y_pos)  # it specifies y values
    ax.set_yticklabels(y_labels)  # specify people y tick labels
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Absolute skewness')  # lbel for x axis
    ax.set_title('Absolute skewness of each feature')  # specifies title

    # Making a legend
    # noon_patch = mpatches.Patch(color=noon_color, label='Day Time')
    # night_patch = mpatches.Patch(color=night_color, label='Night Time')
    # not_answered_patch = mpatches.Patch(color=not_answered_color, label='Not Answered')
    # plt.legend(handles=[night_patch, noon_patch, not_answered_patch])

    # Adjusting shape of plot
    plt.subplots_adjust(left=0.25, right=0.8)

    #Adding grid
    plt.grid()

    #Showing a plot
    plt.show()

# labels_1 = labels[:22]
# values_1 = values[:22]
# def make_histogram(labels,values):
#     # Classificating continuous values to appropriate range.
#     # vs = Visuals()
#     # ranges, sum_of_each_range = vs.classificate(df[columun], num_of_classes, r_min, r_max, 'tuples')
#
#     # Making labels
#     # labels = list(ranges)
#
#     # Setting the positions and width for the bars
#     pos = range(len(values))
#     width = 0.25
#
#     # Plotting the bars
#     fig, ax = plt.subplots(figsize=(10, 5))
#
#     # Create a bars
#     plt.bar(
#         pos,
#         values,
#         width,
#         alpha=0.5,
#         color='#7C5852',
#         label=labels
#     )
#
#     # Setting the x axis label
#     ax.set_xlabel('Features')
#
#     # Set the y axis label
#     ax.set_ylabel('Skewness')
#
#     # Setting the chart's title
#     ax.set_title('Skewness of each feature which contains continuous values')
#
#     # Setting the position of the x ticks
#     ax.set_xticks(pos)
#
#     # Setting the labels for the x ticks
#     ax.set_xticklabels(labels)
#
#     # Adding grid to the plot
#     plt.grid()
#
#     # Adjusting shape of plot
#     plt.subplots_adjust(top=0.85)
#
#     # Showing the plot
#     plt.show()
#
# make_histogram(labels_1,values_1)
# make_histogram(labels_2,values_2)
# make_histogram(labels_3,values_3)
# make_histogram(labels_4,values_4)
# make_histogram(labels_2,values_2)
make_horizontal_histogram(labels,values)