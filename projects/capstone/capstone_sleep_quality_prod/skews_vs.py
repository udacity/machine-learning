import pandas as pd
import numpy as np
import pre_process
import columns_config
import matplotlib.pyplot as plt
import sys

#Getting Raw Data
all_data = pd.read_csv("2013SleepinAmericaPollExerciseandSleepRawDataExcel.csv")

#Dropping target values and storing to another variable.
features = all_data.drop('q30', axis = 1)
sleep_quality = all_data['q30']

#Declaring new features
all_data['Q43TOTAL'] = 0
all_data['Q36Q38Q40TOTAL'] = 0
all_data['Q3Q1DIF'] = 0
all_data['Q4Q2DIF'] = 0
all_data['Q4Q2DIFQ3Q1DIFTOTAL'] = 0

#Making a preprocess object
pre_process_obj = pre_process.PreProcess(all_data,columns_config.columns_config)

#Converting new feature
pre_process_obj.convert_values()
pre_process_obj.convert_types()

#Calculating values of new features
sitting_hours_columns = ['Q43A','Q43B','Q43C','Q43D','Q43E','Q43F','Q43G1','Q43G2','Q43G3']
pre_process_obj.df['Q43TOTAL'] = pre_process_obj.df[sitting_hours_columns].sum(axis=1)
amount_of_exercise_columns= ['Q36','Q38','Q40']
pre_process_obj.df['Q36Q38Q40TOTAL'] = pre_process_obj.df[amount_of_exercise_columns].sum(axis=1)
pre_process_obj.df['Q3Q1DIF'] = pre_process_obj.df['Q3VALUE'] - pre_process_obj.df['Q1VALUE']
pre_process_obj.df['Q4Q2DIF'] = pre_process_obj.df['Q4VALUE'] - pre_process_obj.df['Q2VALUE']
pre_process_obj.df['Q4Q2DIFQ3Q1DIFTOTAL'] = pre_process_obj.df[['Q4Q2DIF','Q3Q1DIF']].sum(axis=1)

#Getting skews
pre_process_obj.get_skews()

#Convert to absolute skews
abs_skews = pre_process_obj.get_skews().abs()

#Sorting skews in descending order
abs_skews.sort_values(ascending=False, inplace=True)

# Showing the list of absolute skews
print abs_skews
sys.exit()

#Getting lables and values to make a horizontal histogram
labels = abs_skews.keys()
values = abs_skews.values
height = 0.8

def make_horizontal_histogram(y_labels,values):
    # The matplotlib.rcdefaults() command restores the standard matplotlib default settings.
    plt.rcdefaults()

    # Getting  matplotlib.figure.Figure object and Axes object or array of Axes objects.
    fig, ax = plt.subplots(1)

    # Setting colors of the bars
    noon_bars = [4, 5, 6]
    not_answered_bars = [21, 22]
    colors_in_hex = [
        '#DD0001','#DD0503','#DD0A05','#DE0F08','#DE140A','#DE1A0D','#DF1F0F','#DF2412',
        '#E02914', '#E02F17', '#E03419', '#E1391B', '#E13E1E', '#E14420', '#E24923', '#E24E25',
        '#E35328', '#E3582A', '#E35E2D', '#E4632F', '#E46831', '#E56D34', '#E57336', '#E57839',
        '#E67D3B', '#E6823E', '#E68840', '#E78D43', '#E79245', '#E89747', '#E89D4A', '#E8A24C',
        '#E9A74F', '#E9AC51', '#EAB154', '#EAB756', '#EABC59', '#EBC15B', '#EBC65D', '#EBCC60',
        '#ECD162', '#ECD665', '#EDDB67', '#EDE16A', '#EDE66C', '#EEEB6F', '#EEF071', '#EFF674'
    ]

    # Setting y coordinates of the bars
    y_pos = np.arange(len(y_labels))

    # Making a horizontal bar plot
    ax.barh(y_pos, values, align='center',height = height, color=colors_in_hex, alpha=0.8)
    ax.set_yticks(y_pos)  # it specifies y values
    ax.set_yticklabels(y_labels)  # specify people y tick labels
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Absolute skew')  # lbel for x axis
    ax.set_title('Absolute skews of each feature')  # specifies title


    # Adjusting shape of the plot
    plt.subplots_adjust(left=0.25, right=0.8)

    #Adding grid
    plt.grid()

    #Showing the plot
    plt.show()

#Showing a horizontal bar plot
make_horizontal_histogram(labels,values)