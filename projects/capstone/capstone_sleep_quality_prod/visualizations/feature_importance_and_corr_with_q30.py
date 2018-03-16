import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

# Loading the dataset contains feature importance and correlation with q30
df = pd.read_csv("../feature_importance_and_corr_with_q30_f_50_r_0.csv")
df.rename(columns={'Unnamed: 0':'feature_name'},inplace=True)
df.sort_values('feature_importance', ascending=True,inplace=True)

def make_horizontal_bars(range,title):

    # Making indent of bars
    ind = np.arange(15) * 2

    # Setting width of bars
    width = 0.4

    # Creating a figure and a setting of subplots
    fig, ax = plt.subplots()

    # Setting the size of a plot
    fig.set_size_inches(7.5, 7.5)

    # Making another y axis
    ax2 = ax.twiny()

    # Making a bar represents feature importance
    rects2 = ax2.barh(ind + width, df.iloc[range[0]:range[1]]['feature_importance'], width, color='red', label='Feature importance')

    # Making a bar represents correlation with q30
    rects1 = ax.barh(ind, df.iloc[range[0]:range[1]]['corr_with_q30'], width, color='green', label='Correlation with q30')

    # Setting ticks of feature importance bars
    ax2.set(yticks=ind + (width /2), yticklabels=df[range[0]:range[1]].feature_name, xlabel='Feature importance', xlim=[-0.05, 0.05])

    # Setting ticks of correlation bar
    ax.set(xlabel='Correlation with q30', xlim=[-0.5, 0.5])

    # Setting a legend
    plt.legend(loc="upper center", handles=[rects2, rects1], labels=["Feature importance", "Correlation with q30"],
               bbox_to_anchor=(1.35, 1),fancybox = True)

    # Adjusting shape of a plot
    plt.subplots_adjust(top=0.75,left=0.25,right=0.65)

    # Setting a title
    plt.title(title,y=1.08)

    # Showing plot
    plt.show()

# Making bars of top 1 to 15 important features
title = 'Feature importance and correlation with q30 \n' \
        'of final model with top 50 important features.\n' \
        '(Only shows the ones of top 1 to 15 important features) \n'
range = [35,50]
make_horizontal_bars(range,title)

# Making bars of top 16 to 30 important features
title = 'Feature importance and correlation with q30 \n' \
        'of final model with top 50 important features.\n' \
        '(Only shows the ones of top 16 to 30 important features) \n'
range = [20,35]
make_horizontal_bars(range,title)
